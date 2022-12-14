from flask import Flask, request, jsonify, json
from asset import exchAsset
from streamer import streamer
import threading

app = Flask(__name__)

binanceStreams = []
binanceAssets = {}

@app.route("/addAsset/<exch>/<asset>", methods=['POST'])
def ext_addAsset(exch: str, asset: str):
    key = exch + ":" + asset
    if exch == "BINANCE":
        a = exchAsset(exch, asset, key)
        binanceAssets[key] = a
        s = streamer(asset, a)
        t = threading.Thread(target=s.sock.run_forever)
        t.daemon = True
        t.start()
        binanceStreams.append(s)
        # s.streamBinance()
    print(exch, asset)
    res = {"error": "none"}
    return jsonify(res)
    
    
@app.route("/latestPrice/<exch>/<asset>")
def ext_getLatest(exch: str, asset: str):
    key = exch + ":" + asset
    a = binanceAssets[key]
    res = {
        "bestBid" : a.bestBid,
        "bidSize" : a.bidSize,
        "bestOffer" : a.bestOffer,
        "offerSize" : a.offerSize
    }
    return jsonify(res)
    
    
def main():
    pass

if __name__ == "__main__":
    app.run()