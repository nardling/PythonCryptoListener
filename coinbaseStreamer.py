import websocket
import json

def onMessage(ws, message):
    print(message)

def onError(ws, error):
    print(error)
    
def onClose(message):
    print(message)
    
def streamCoinbase(symbol):
    addr = f'wss://ws-feed.exchange.coinbase.com'
    # ws = websocket.WebSocketApp(addr,
    #                     on_message=onMessage,
    #                     on_error=onError,
    #                     on_close=onClose)
    ws = websocket.WebSocket()
    ws.connect(addr)
    print(ws.getstatus())
    sub = {
        "type": "subscribe",
        "channels": [
            {
                "name": "ticker",
                "product_ids": [
                    "BTC-USD"
                ]
            }
        ]
    }
    msg=json.dumps(sub)
    ws.send(msg)
    quote = ws.recv()
    while quote:
        print(quote)
        quote=ws.recv()
    # ws.run_forever()
    
streamCoinbase('BTC-USD')
