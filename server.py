from lib.websocket_server import WebsocketServer
import json
import logging
import threading
import pandas as pd
import time
import os
# Name:
# tickfeed server
# Description:
# reads from tick data file, broadcast tick messages
class TickServer(WebsocketServer):
    def __init__(self, port, host='127.0.0.1', loglevel=logging.WARNING):
        WebsocketServer.__init__(self, port, host, loglevel)

# feed callback func
def tick_feed(tfile,channel,client):
    try:
        reader = pd.read_csv(tfile, iterator=True)
        loop=True
        chunkSize=1000
        while loop:
            try:
                chunk = reader.get_chunk(chunkSize)
                chunk = chunk.drop("Unnamed: 0", axis=1)
                chunk['symbol'] = '600226'

                for index,row in chunk.iterrows():
                    time.sleep(1)
                    message = '{"table":"' + channel + '","data":' + row.to_json() + '}'
                    print(message)
                    server.send_message(client,message)
            except StopIteration:
                loop = False
                print("Iteration stoped")
    except Exception as e:
        print(e)
        print("Tick feed exception, quit")

# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    server.send_message(client,'{"event":"ready"}')

# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])

# Called when a client sends a message
def message_received(client, server, message):
    data = json.loads(message)
    op = data["op"]
    if op == "subscribe":
        channels = data["args"]
        for channel in channels:
            if channel == subscribed_clients.get(client['id'], None):
                return
            lst = channel.split("-")
            if lst[0] == "ticker":
                threading.Thread(target=tick_feed,args=(tfile,channel,client,)).start()
                print("Client({}) subscribe for {}".format(client['id'], channel))
                subscribed_clients[client['id']]=channel

subscribed_clients = {}
script_path = os.path.split(os.path.realpath(__file__))[0]
tfile=script_path + '/data/600226_2019_08_13_2019_08_23_tick.csv'
print(tfile)
PORT=9002
server = TickServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
