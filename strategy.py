from asset import exchAsset
from tradesServer import tradesServer
import time
import json
import logging

class strategy:
    def __init__(self, asset: exchAsset, target: str, condition: str, value: float, action: str, tradeBroadcaster: tradesServer, name: str, time_delay: int, max_trade: float):
        self.asset = asset
        self.target = target
        self.condition = condition
        self.value = value
        self.action = action
        self.lastTradeTime = 0
        self.running = False
        self.tradeBroadcaster = tradeBroadcaster
        self.name = name
        self.time_delay: int = time_delay
        self.max_trade: float = max_trade
        self.lastTradeTime: int = 0

    def setThreshold(self, newValue: float):
        self.value = newValue

    def eval(self):
        if self.running == False:
            return

        target_value = 0
        
        if self.target == "BID":
            target_value = self.asset.bestBid
        if self.target == "OFFER":
            target_value = self.asset.bestOffer
        if self.target == "DIFF":
            target_value = self.asset.bestOffer - self.asset.bestBid

        ts: int = time.time()
        if self.lastTradeTime != 0 and (ts - self.lastTradeTime) <= self.time_delay:
            return

        # print ("Strategy ", self.name, " in eval. self.value=", str(self.value), " ", self.condition, " ", str(target_value))
        if self.condition == "LT" and target_value < self.value:
            for s in self.asset.getState():
                print (s)
            self.execute(target_value, ts)

        if self.condition == "GT" and target_value > self.value:
            self.execute(target_value, ts)
            for s in self.asset.getState():
                print (s)
    
    def start(self):
        self.running = True
        print ("Strategy ", self.name, " started")

    def stop(self):
        self.running = False
        print ("Strategy ", self.name, " stopped")

    def isRunning(self):
        return self.running

    def execute(self, target_value, ts):
        self.lastTradeTime = ts
        execQty: float = self.asset.offerSize if self.action == "BUY" else self.asset.bidSize
        print ("Execute ", self.name)
        tradeInfo = { }
        tradeInfo["type"] = "TRADE"
        tradeInfo["strategy_name"] = self.name
        tradeInfo["exec_qty"] = execQty
        tradeInfo["trade_time"] = ts
        tradeInfo["calc_edge"] = target_value

        for ld in self.asset.legData(self.action):
            tradeInfo["exec_price"] = ld["exec_price"]
            tradeInfo["asset_name"] = ld["asset_name"]
            tradeInfo["trade_action"] = ld["trade_action"]
            print (tradeInfo)
            self.tradeBroadcaster.sendFunc(json.dumps(tradeInfo))
        