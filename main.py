from flask import Flask, request, jsonify, json
from flask_cors import CORS
from asset import exchAsset
from streamer import streamer
from coinbaseStreamer import coinbaseStreamer
import threading

app = Flask(__name__)
cors = CORS(app)

binanceStreams = []
coinbaseStream = None
binanceAssets = {}

@app.route("/addAsset/<exch>/<asset>", methods=['POST'])
def ext_addAsset(exch: str, asset: str):
    global coinbaseStream
    key = exch + ":" + asset
    if exch == "BINANCE":
        if key not in binanceAssets:
            a = exchAsset(exch, asset, key)
            binanceAssets[key] = a
            s = streamer(asset, a)
            t = threading.Thread(target=s.sock.run_forever)
            t.daemon = True
            t.start()
            binanceStreams.append(s)
        else:
            print("Asset already registered")
    if exch == "COINBASE":
        if key not in binanceAssets:
            a = exchAsset(exch, asset, key)
            binanceAssets[key] = a
            if coinbaseStream is None:
                coinbaseStream = coinbaseStreamer(asset, a)
                coinbaseStream.subscribe(asset)
                t = threading.Thread(target=coinbaseStream.streamCoinbase)
                t.daemon = True
                t.start()
            else: 
                coinbaseStream.subscribe(asset)
    print(exch, asset)
    res = {"error": "none"}
    return jsonify(res)
    
    
@app.route("/latestPrice/<exch>/<asset>")
def ext_getLatest(exch: str, asset: str):
    key = exch + ":" + asset
    if key in binanceAssets:
        a = binanceAssets[key]
        res = {
            "bestBid" : a.bestBid,
            "bidSize" : a.bidSize,
            "bestOffer" : a.bestOffer,
            "offerSize" : a.offerSize
        }
        return jsonify(res)
    else:
        res = {
            "error": "key not found"
        }
        return jsonify(res)
    
    
def main():
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0')