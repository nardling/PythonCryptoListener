from flask import Flask, request, jsonify, json
from flask_cors import CORS
from asset import exchAsset
from synthAsset import synthAsset
from streamer import streamer
from coinbaseStreamer import coinbaseStreamer
from strategy import strategy
import threading
from tradesServer import tradesServer
import threading
# import logging

app = Flask(__name__)
cors = CORS(app)

binanceStreams = []
coinbaseStream = None
binanceAssets = {}
synthAssets = {}
strategies = {}
serveinst = None
tradeServer = tradesServer(5002)
awaitingInit: bool
# logging.basicConfig(filename='strategy.log', filemode='w')

@app.route("/addAsset/<exch>/<asset>", methods=['POST'])
def ext_addAsset(exch: str, asset: str):
    int_addAsset(exch=exch, asset=asset)
    res = {"error": "none"}
    return jsonify(res)
    
def int_addAsset(exch: str, asset: str):
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
        # else:
        #     print("Asset already registered")
    if exch == "COINBASE":
        if key not in binanceAssets:
            a = exchAsset(exch, asset, key)
            binanceAssets[key] = a
            if coinbaseStream is None:
                coinbaseStream = coinbaseStreamer(asset, a)
                coinbaseStream.subscribe(asset, a)
                t = threading.Thread(target=coinbaseStream.streamCoinbase)
                t.daemon = True
                t.start()
            else: 
                coinbaseStream.subscribe(asset, a)
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
    key: str = exch + ":" + asset
    if key not in binanceAssets:
        int_addAsset(exch, asset)
    
    if synthDescr in synthAssets:
        synthAssets[synthDescr].addLeg(key, binanceAssets[key], float(weight))
        binanceAssets[key].addSynth(synthAssets[synthDescr])
    
    return jsonify({})

@app.route("/getLatestSynthPrice/<userId>/<descr>")
def ext_getLatestSynthPrice(userId: int, descr: str):
    if descr in synthAssets:
        res = {
            "bestBid" : synthAssets[descr].bestBid,
            "bidSize" : 0,
            "bestOffer" : synthAssets[descr].bestOffer,
            "offerSize" : 0
        }
        # print(res)
        return jsonify(res)
    else:
        return jsonify({})
 
@app.route("/registerStrategy/<userId>/<synthAsset>/<target>/<condition>/<value>/<action>/<maxExposure>/<maxTrade>/<timeDelay>/<name>", methods=["POST"])
def ext_registerStrategy(userId: int, synthAsset: str, target: str, condition: str, value: str, action: str, maxExposure: float, maxTrade: float, timeDelay: int, name: str):
    if name in strategies:
        return jsonify({})
    asset = synthAssets[synthAsset]
    if asset is None:
        return jsonify({})
    strat = strategy(asset, target, condition, float(value), action, tradeServer)
    strategies[name] = strat
    asset.attachStrat(strat)
    return jsonify({})

@app.route("/startStopStrategy/<userId>/<name>/<action>", methods=["POST"])
def ext_start_stop_strat(userId: int, name: str, action: str):
    if name in strategies:
        if action == "START":
            strategies[name].start()
            return jsonify({"status": "Running"})
        else:
            strategies[name].stop()
            return jsonify({"status": "Stopped"})
    else:
        return jsonify({"status": "NotFound"})
    
@app.route("/getStrategyState/<userId>/<name>")
def ext_getStrategyState(userId: int, name: str):
    if name in strategies:
        strat = strategies[name]
        if strat.isRunning():
            return jsonify({"isRegistered": True, "isRunning": True})
        else:
            return jsonify({"isRegistered": True, "isRunning": False})
    else:
        return jsonify({"isRegistered": False})

def main():
    pass

def init():
    serveinst = threading.Thread(target=tradeServer.start, daemon=True)
    if serveinst:
        print("Starting Trades Server")
        serveinst.start()
    else:
        print("Trades Server DID NOT START")

if __name__ == "__main__":
    init()
    app.run(host='0.0.0.0', debug=True, use_reloader=False)
