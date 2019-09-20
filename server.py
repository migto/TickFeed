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
import signal
import copy
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from enum import unique
import requests
import pika
import pandas as pd
from google.protobuf.json_format import MessageToDict
from lib.websocket_server import WebsocketServer
from lib.rcvdata_pb2 import RcvData
from dataclasses_json import dataclass_json

@unique
class Mode(Enum):
    """This class defines the server modes:
    dataframe: using csv text file
    protobuf: using proto3 bin file
    live: using rabbitmq"""
    dataframe = 1
    protobuf = 2
    live = 3

MQ_CONFIG = {
    "host": "192.168.91.130",
    "port": 5672,
    "vhost": "/",
    "user": "guest",
    "passwd": "guest",
    "exchange": "amq.fanout",
    "routingkey": "queue"
}

TRADE_URL = "http://192.168.91.130:8888"

PORT = 9002
TICK = 0.5
#MODE = Mode.dataframe
#MODE = Mode.protobuf
MODE = Mode.live
DIRECTORY = os.path.split(os.path.realpath(__file__))[0]
DF_FILE = DIRECTORY + '/data/600226_2019_08_13_2019_08_23_tick.csv'
PR_FILE = DIRECTORY + '/data/rcv_data_20190911'
TFILE = DF_FILE
if MODE is Mode.protobuf:
    TFILE = PR_FILE

@dataclass_json
@dataclass
class Order:
    symbol: str
    oid: str
    otype: str
    op: str
    price: float
    volume: int
    traded: int
    status: str
    time: str
    last_fill_qty: int = 0
    avr_fill_price: float = 0
    def is_active(self):
        if self.status not in {"全部成交","全部撤单"}:
            return True
        return False

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
            self._amqp_credentials = pika.PlainCredentials(\
                MQ_CONFIG.get("user"), MQ_CONFIG.get("passwd"))
            self._amqp_parameters = pika.ConnectionParameters(\
                MQ_CONFIG.get("host"), MQ_CONFIG.get("port"),\
                MQ_CONFIG.get("vhost"), self._amqp_credentials)
            self._amqp_connection = pika.BlockingConnection(self._amqp_parameters)
            self._amqp_channel = self._amqp_connection.channel()
            result = self._amqp_channel.queue_declare(queue='', exclusive=True)
            self._amqp_channel.queue_bind(exchange=MQ_CONFIG.get("exchange"),\
                       queue=result.method.queue)
            self._amqp_channel.basic_consume(queue=result.method.queue,
                                             auto_ack=True,
                                             on_message_callback=self.callback)

    def send_report(self, report):
        """This method sends out the report structure to vnpy trader
        do the format transform thing"""
        message="report"
        try:
            dic = {}
            dic['symbol'] = report.label.decode('gbk')
            dic['name'] = report.name.decode('gbk')
            dic['time'] = datetime.fromtimestamp(report.time)\
                                  .strftime("%Y-%m-%d %H:%M:%S")
            dic['pre_close'] = float('%.2f' % report.last_close)
            dic['open_price'] = float('%.2f' % report.open)
            dic['high_price'] = float('%.2f' % report.high)
            dic['low_price'] = float('%.2f' % report.low)
            dic['last_price'] = float('%.2f' % report.new_price)
            dic['open_interest'] = float('%.2f' % report.amount)
            dic['volume'] = float('%.2f' % report.volume)

            dic['b1_p'] = float('%.2f' % report.buy_price_1)
            dic['b2_p'] = float('%.2f' % report.buy_price_2)
            dic['b3_p'] = float('%.2f' % report.buy_price_3)
            dic['b4_p'] = float('%.2f' % report.buy_price_4)
            dic['b5_p'] = float('%.2f' % report.buy_price_5)
            dic['b1_v'] = float('%.2f' % report.buy_volume_1)
            dic['b2_v'] = float('%.2f' % report.buy_volume_2)
            dic['b3_v'] = float('%.2f' % report.buy_volume_3)
            dic['b4_v'] = float('%.2f' % report.buy_volume_4)
            dic['b5_v'] = float('%.2f' % report.buy_volume_5)
            dic['a1_p'] = float('%.2f' % report.sell_price_1)
            dic['a2_p'] = float('%.2f' % report.sell_price_2)
            dic['a3_p'] = float('%.2f' % report.sell_price_3)
            dic['a4_p'] = float('%.2f' % report.sell_price_4)
            dic['a5_p'] = float('%.2f' % report.sell_price_5)
            dic['a1_v'] = float('%.2f' % report.sell_volume_1)
            dic['a2_v'] = float('%.2f' % report.sell_volume_2)
            dic['a3_v'] = float('%.2f' % report.sell_volume_3)
            dic['a4_v'] = float('%.2f' % report.sell_volume_4)
            dic['a5_v'] = float('%.2f' % report.sell_volume_5)
            message = '{"table":"' + self._channel +\
                 '","data":' + json.dumps(dic) + '}'
            self._server.send_message(self._client, message)
        except IOError as err:
            print(message)
            print(err)
            self.stop()
        except Exception as err:
            print(message)
            print(err)
            #self.stop()

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
                            #print(message)
                            self._server.send_message(self._client, message)
                            if self.stopped():
                                print("Thread for channel {} has been stopped, quit".format(self._channel))
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
                        if self.stopped():
                            print("Thread for channel {} has been stopped, quit".format(self._channel))
                            return
                        for report in self._rcv_data.lstReport:
                            label = report.label.decode('gbk')
                            if label == self._symbol:
                                self.send_report(report)
                                time.sleep(TICK)
            elif self._mode is Mode.live:
                print("Live mode active, receiving messages")
                self._amqp_channel.start_consuming()
            else:
                print("Unsupported mode {}, quit".format(self._mode))
        except Exception as e:
            print(e)
            print("Tick feed exception, quit")
            self.stop()

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
        self._subscribed_channels = {}
        self._started_threads = {}
        self._orders = {}
        self._thread = threading.Thread(target=self._run)
        self._active = True
        self._thread.start()

    def _push_order(self, order: Order):
        """Push order info to vnpy
        """
        if len(self.clients) == 0:
            return
        client = self.clients[0]
        message = '{"table":"order", "data":' + order.to_json() + '}'
        self.send_message(client, message)

    def _run(self):
        """This method periodically gets the open order status from tradeAPI
        and send websocket updates to vnpy
        """
        try:
            while self._active:
                response = requests.get(TRADE_URL + "/api/v1.0/orders")
                content = json.loads(response.text)
                od_lst = content['dataTable']['rows']
                for od in od_lst:
                    cur_order = Order(od[1], # symbol
                                      od[11], # oid
                                      od[9], # otype
                                      od[3], # op
                                      float(od[8]), # price
                                      int(od[5]), # volume
                                      int(od[6]), # traded
                                      od[4], # status
                                      od[0], # time
                                      )
                    last_order = self._orders.get(od[11], None)
                    self._orders[od[11]] = cur_order
                    if last_order and last_order.is_active():
                        cur_order.last_fill_qty = cur_order.traded - last_order.traded
                        cur_order.avr_fill_price = float(od[10])
                        self._push_order(cur_order)
                time.sleep(2)
        except Exception as err:
            print(err)
            print("Order update error, quit")

    def new_client(self, client, server):
        """Called for every client connecting
        """
        print("New client connected and was given id %d" % client['id'])
        server.send_message(client, '{"event":"ready"}')

    def client_left(self, client, server):
        """Called for every client disconnecting
        """
        channel_set = self._subscribed_channels.pop(client['id'], None)
        if not channel_set:
            print("Client(%d) does not subscribe to any channel" % client['id'])
        else:
            print("Client(%d)'s channel subscribtion cancelled" % client['id'])
        thread_set = self._started_threads.pop(client['id'], None)
        if not thread_set:
            print("Client(%d) does not start any threads" % client['id'])
        else:
            for thread in thread_set:
                thread.stop()
            print("Client(%d)'s threads stopped" % client['id'])
        print("Client(%d) disconnected" % client['id'])

    def message_received(self, client, server, message):
        """Called when a client sends a message
        """
        data = json.loads(message)
        if data["op"] == "subscribe":
            channels = data["args"]
            channel_set = self._subscribed_channels.get(client['id'],set())
            if not channel_set:
                self._subscribed_channels[client['id']] = channel_set
            for channel in channels:
                if channel in channel_set:
                    print("Client{} already subscribed for channel {}".format(client['id'],channel))
                    # already subscribed
                    return
                # one thread for each subscription
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
                    channel_set.add(channel)
                    print("Client({}) subscription list:{}".format(client['id'], channel_set))
                    thread_set = self._started_threads.get(client['id'], set())
                    if not thread_set:
                        self._started_threads[client['id']] = thread_set
                    thread_set.add(tick_thread)

def main():
    SERVER = TickServer(PORT)
    SERVER.run_forever()

if __name__ == '__main__':
    main()
