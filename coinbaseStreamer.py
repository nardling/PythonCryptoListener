import websocket
import json

class coinbaseStreamer:
    def __init__(self, symbol, asset):
        self.asset = asset
        self.symbol = symbol
        self.addr = f'wss://ws-feed.exchange.coinbase.com'
        self.sock = websocket.WebSocket()
        self.sock.connect(self.addr)
        self.subscribed = False
        self.symbols = set()
    
    def subscribe(self, symbol):
        if symbol in self.symbols:
            return
        
        self.symbols.add(symbol)
        
        if self.subscribed:
            # unsubscribe
            unsub = {
                "type": "unsubscribe",
                "channels": [
                    {
                        "name": "ticker"
                    }
                ]
            }
            msg=json.dumps(sub)
            self.sock.send(msg)
            
        sub = {
            "type": "subscribe",
            "channels": [
                {
                    "name": "ticker",
                    "product_ids": []
                }
            ]
        }
        
        print (sub)
        
        for s in self.symbols:
            sub['channels'][0]['product_ids'].append(s)
        
        msg=json.dumps(sub)
        print(msg)
        self.sock.send(msg)
    
    def streamCoinbase(self):
        quote = self.sock.recv()
        while quote:
            # print(quote)
            quote=self.sock.recv()