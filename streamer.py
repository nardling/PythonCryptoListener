import websocket
import threading
from flask import json

class streamer:
    def __init__(self, symbol, asset):
        self.asset = asset
        self.symbol = symbol
        addr = f'wss://stream.binance.us:9443/ws/{self.symbol}@ticker'
        self.sock = websocket.WebSocketApp(addr,
                            on_message=self.onMessage,
                            on_error=self.onError,
                            on_close=self.onClose)
        
    def onMessage(self, ws, message):
        print(message)
        msgDict = json.loads(message)
        self.asset.bestBid = msgDict["b"]
        self.asset.bidSize = msgDict["B"]
        self.asset.bestOffer = msgDict["a"]
        self.asset.offerSize = msgDict["A"]

    def onError(self, ws, error):
        print(error)
        
    def onClose(self, message, parm1, parm2):
        print(message)
        print(parm1)
        print(parm2)

    def run(self):
        self.sock.run_forever()
        print ("socket started")
    
