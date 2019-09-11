"""This server provides tick-level stock streaming service to
vnpy trader
"""
import json
import logging
import threading
import time
import os
import sys
import base64
from datetime import datetime
from enum import Enum
from enum import unique
import pika
import pandas as pd
from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import MessageToJson
from lib.websocket_server import WebsocketServer
from lib.rcvdata_pb2 import RcvData

MQ_CONFIG = {
    "host": "192.168.91.130",
    "port": 5672,
    "vhost": "/",
    "user": "guest",
    "passwd": "guest",
    "exchange": "amq.fanout",
    "routingkey": "queue"
}

@unique
class Mode(Enum):
    """This class defines the server modes:
    dataframe: using csv text file
    protobuf: using proto3 bin file
    live: using rabbitmq"""
    dataframe = 1
    protobuf = 2
    live = 3

class StoppableThread(threading.Thread):
    """This class is invoked when a vnpy trader gateway
    connect to server succcessfully and subscribed for a
    specific symbol channel
    """
    def __init__(self, mode, file, channel, client, server):
        super().__init__()
        self._stop_event = threading.Event()
        self._mode = mode
        self._file = file
        self._channel = channel
        self._client = client
        self._rcv_data = RcvData()
        self._chunk_size = 1000
        self._server = server

        lst = self._channel.split('-')
        if len(lst) != 2:
            print('Unrecognized channel {}'.format(self._channel))
        self._symbol = lst[1]

        # if Mode is live, initialize amqp connection to rabbitmq
        self._amqp_channel = None
        self._amqp_connection = None
        if self._mode is Mode.live:
            self._amqp_credentials = pika.PlainCredentials(MQ_CONFIG.get("user"), MQ_CONFIG.get("passwd"))
            self._amqp_parameters = pika.ConnectionParameters(MQ_CONFIG.get("host"), MQ_CONFIG.get("port"),\
                                           MQ_CONFIG.get("vhost"), self._amqp_credentials)
            self._amqp_connection = pika.BlockingConnection(self._amqp_parameters)
            self._amqp_channel = self._amqp_connection.channel()
            result = self._amqp_channel.queue_declare(queue='', exclusive=True)
            self._amqp_channel.queue_bind(exchange=MQ_CONFIG.get("exchange"),
                       queue=result.method.queue)
            self._amqp_channel.basic_consume(queue=result.method.queue,
                                        auto_ack=True,
                                        on_message_callback=self.callback)

    def send_report(self, report):
        """This method sends out the report structure to vnpy trader
        do the format transform thing"""
        dic = MessageToDict(report)
        dic['symbol'] = base64.b64decode(dic['label'])\
                             .decode('gbk')
        dic['name'] = base64.b64decode(dic['name'])\
                            .decode('gbk')
        dic['time'] = datetime.fromtimestamp(dic['time'])\
                              .strftime("%Y-%m-%d %H:%M:%S")
        dic['pre_close'] = float('%.2f' % dic.pop('lastClose'))
        dic['open_price'] = float('%.2f' % dic.pop('open'))
        dic['high_price'] = float('%.2f' % dic.pop('high'))
        dic['low_price'] = float('%.2f' % dic.pop('low'))
        dic['last_price'] = float('%.2f' % dic.pop('newPrice'))
        dic['open_interest'] = float('%.2f' % dic.pop('amount'))
        dic['volume'] = float('%.2f' % dic.pop('volume'))

        dic['b1_p'] = float('%.2f' % dic.pop('buyPrice1'))
        dic['b2_p'] = float('%.2f' % dic.pop('buyPrice2'))
        dic['b3_p'] = float('%.2f' % dic.pop('buyPrice3'))
        dic['b4_p'] = float('%.2f' % dic.pop('buyPrice4'))
        dic['b5_p'] = float('%.2f' % dic.pop('buyPrice5'))
        dic['b1_v'] = float('%.2f' % dic.pop('buyVolume1'))
        dic['b2_v'] = float('%.2f' % dic.pop('buyVolume2'))
        dic['b3_v'] = float('%.2f' % dic.pop('buyVolume3'))
        dic['b4_v'] = float('%.2f' % dic.pop('buyVolume4'))
        dic['b5_v'] = float('%.2f' % dic.pop('buyVolume5'))
        dic['a1_p'] = float('%.2f' % dic.pop('sellPrice1'))
        dic['a2_p'] = float('%.2f' % dic.pop('sellPrice2'))
        dic['a3_p'] = float('%.2f' % dic.pop('sellPrice3'))
        dic['a4_p'] = float('%.2f' % dic.pop('sellPrice4'))
        dic['a5_p'] = float('%.2f' % dic.pop('sellPrice5'))
        dic['a1_v'] = float('%.2f' % dic.pop('sellVolume1'))
        dic['a2_v'] = float('%.2f' % dic.pop('sellVolume2'))
        dic['a3_v'] = float('%.2f' % dic.pop('sellVolume3'))
        dic['a4_v'] = float('%.2f' % dic.pop('sellVolume4'))
        dic['a5_v'] = float('%.2f' % dic.pop('sellVolume5'))
        message = '{"table":"' + self._channel +\
             '","data":' + json.dumps(dic) + '}'
        print(message)
        self._server.send_message(self._client, message)

    def callback(self, ch, method, proerties, body):
        """This method is the amqp consuming callback method
        parse the data and send the report matches thread
        symbol
        """
        self._rcv_data.ParseFromString(body)
        for report in self._rcv_data.lstReport:
            label = report.label.decode('gbk')
            if label == self._symbol:
                self.send_report(report)

    def run(self):
        try:
            if self._mode is Mode.dataframe:
                reader = pd.read_csv(self._file, iterator=True)
                loop = True
                while loop:
                    try:
                        chunk = reader.get_chunk(self._chunk_size)
                        chunk = chunk.drop("Unnamed: 0", axis=1)
                        chunk['symbol'] = '600226'

                        for index, row in chunk.iterrows():
                            time.sleep(1)
                            message = '{"table":"' + self._channel +\
                                 '","data":' + row.to_json() + '}'
                            print(message)
                            self._server.send_message(self._client, message)
                            if self.stopped():
                                print("Thread has been stopped, quit")
                                return
                    except StopIteration:
                        loop = False
                        print("Iteration stoped")
            elif self._mode is Mode.protobuf:
                with open(self._file, 'rb') as rcv_file:
                    rcv_file.seek(0, 2)
                    file_size = rcv_file.tell()
                    rcv_file.seek(0)
                    cur_pos = 0
                    while cur_pos < file_size:
                        msg_length = int.from_bytes(rcv_file.read(4),
                                                    sys.byteorder)
                        msg_data = rcv_file.read(msg_length)
                        self._rcv_data.ParseFromString(msg_data)
                        for report in self._rcv_data.lstReport:
                            label = report.label.decode('gbk')
                            if label == self._symbol:
                                self.send_report(report)
                                time.sleep(0.01)
            elif self._mode is Mode.live:
                print("Live mode active, receiving messages")
                self._amqp_channel.start_consuming()
            else:
                print("Unsupported mode {}, quit".format(self._mode))
        except Exception as e:
            print(e)
            print("Tick feed exception, quit")

    def stop(self):
        """Set the stop event
        """
        self._stop_event.set()

    def stopped(self):
        """Check if stop event is set
        """
        return self._stop_event.is_set()

class TickServer(WebsocketServer):
    """This class is the main server, accepts client connections,
    respond using new threads
    """
    def __init__(self, port, host='127.0.0.1', loglevel=logging.WARNING):
        WebsocketServer.__init__(self, port, host, loglevel)
        self._subscribed_clients = {}
        self._client_thread_map = {}

    def new_client(self, client, server):
        """Called for every client connecting
        """
        print("New client connected and was given id %d" % client['id'])
        server.send_message(client, '{"event":"ready"}')

    def client_left(self, client, server):
        """Called for every client disconnecting
        """
        print("Client(%d) disconnected" % client['id'])

    def message_received(self, client, server, message):
        """Called when a client sends a message
        """
        data = json.loads(message)
        if data["op"] == "subscribe":
            channels = data["args"]
            for channel in channels:
                if channel == self._subscribed_clients.get(client['id'],
                                                           None):
                    # already subscribed
                    return

                lst = channel.split("-")
                if lst[0] == "ticker":
                    tick_thread = StoppableThread(MODE,
                                                  TFILE,
                                                  channel,
                                                  client,
                                                  server)
                    tick_thread.start()
                    print("Client({}) subscribe for {}"\
                        .format(client['id'], channel))
                    self._subscribed_clients[client['id']] = channel
                    self._client_thread_map[client['id']] = tick_thread

PORT = 9002
#MODE = Mode.dataframe
MODE = Mode.protobuf
#MODE = Mode.live
DIRECTORY = os.path.split(os.path.realpath(__file__))[0]
DF_FILE = DIRECTORY + '/data/600226_2019_08_13_2019_08_23_tick.csv'
PR_FILE = DIRECTORY + '/data/rcv_data_20190910_sample'
TFILE = DF_FILE
if MODE is Mode.protobuf:
    TFILE = PR_FILE
SERVER = TickServer(PORT)
SERVER.run_forever()
