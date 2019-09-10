# encoding=utf-8
import websocket


# 在接受到服务器发送消息时调用
def on_message(ws, message):
    print('Recieved: ' + message)

def on_open(ws):
    print('Server connected')

if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://127.0.0.1:9002",
                                 on_message = on_message,
                                 on_open = on_open)
    ws.run_forever()

