from flask import Flask, request, jsonify, json
from flask_cors import CORS
from asset import exchAsset
from synthAsset import synthAsset
from streamer import streamer
from coinbaseStreamer import coinbaseStreamer
import threading

app = Flask(__name__)
cors = CORS(app)

binanceStreams = []
coinbaseStream = None
binanceAssets = {}
synthAssets = {}

@app.route("/addAsset/<exch>/<asset>", methods=['POST'])
def ext_addAsset(exch: str, asset: str):
    int_addAsset(exch=exch, asset=asset)
    res = {"error": "none"}
    return jsonify(res)
    
def int_addAsset(exch: str, asset: str):
    global coinbaseStream
    key = exch + ":" + asset
    print ("In ext_addAsset for ", key)
    if exch == "BINANCE":
        if key not in binanceAssets:
            a = exchAsset(exch, asset, key)
            binanceAssets[key] = a
            s = streamer(asset, a)
            t = threading.Thread(target=s.sock.run_forever)
            t.daemon = True
            t.start()
            binanceStreams.append(s)
            print ("Registered ", key)
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

@app.route("/registerSynthAsset/<userId>/<descr>", methods=['POST'])
def ext_registerSynthAsset(userId: int, descr: str):
    if descr in synthAssets:
        res = {
            "error": "key already present"
        }
        return jsonify(res)
    else:
        s = synthAsset(descr)
        synthAssets[descr] = s
        return jsonify({})
    
@app.route("/registerSynthLeg/<userId>/<synthDescr>/<exch>/<asset>/<weight>", methods=['POST'])
def ext_registerSynthLeg(userId: int, synthDescr: str, exch: str, asset: str, weight: float):
    key = exch + ":" + asset
    if key not in binanceAssets:
        int_addAsset(exch, asset)
    
    if synthDescr in synthAssets:
        synthAssets[synthDescr].addLeg(binanceAssets[key], float(weight))
    
    return jsonify({})

@app.route("/getLatestSynthPrice/<userId>/<descr>")
def ext_getLatestSynthPrice(userId: int, descr: str):
    if descr in synthAssets:
        print (synthAssets[descr].getPrice("SELL"))
        res = {
            "bestBid" : synthAssets[descr].getPrice("SELL"),
            "bidSize" : 0,
            "bestOffer" : synthAssets[descr].getPrice("BUY"),
            "offerSize" : 0
        }
        print(res)
        return jsonify(res)
    else:
        return jsonify({})

def main():
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)