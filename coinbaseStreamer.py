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
        self.symbols = {}
    
    def subscribe(self, symbol, asset):
        if symbol in self.symbols:
            return
        
        self.symbols[symbol] = asset
        
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
                
        for s in self.symbols:
            sub['channels'][0]['product_ids'].append(s)
        
        msg=json.dumps(sub)
        self.sock.send(msg)
    
    def streamCoinbase(self):
        quote = self.sock.recv()
        while quote:
            msgDict = json.loads(quote)
            sym = msgDict.get('product_id')
            if sym:
                curAsset = self.symbols.get(sym)
                curAsset.updateTop(msgDict['best_bid'], msgDict['best_bid_size'], msgDict['best_ask'], msgDict['best_ask_size'])
                curAsset.updateSynths()
            quote=self.sock.recv()