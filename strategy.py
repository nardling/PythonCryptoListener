from asset import exchAsset
from tradesServer import tradesServer
import time
import logging

class strategy:
    def __init__(self, asset: exchAsset, target: str, condition: str, value: float, action: str, tradeBroadcaster: tradesServer):
        self.asset = asset
        self.target = target
        self.condition = condition
        self.value = value
        self.action = action
        self.lastTradeTime = 0
        self.running = False
        print (tradeBroadcaster)
        print (type(tradeBroadcaster))
        self.tradeBroadcaster = tradeBroadcaster
            
    def eval(self):
        if self.running == False:
            return

        target_value = 0
        
        if self.target == "Buy":
            target_value = self.asset.bestBid
        if self.target == "Sell":
            target_value = self.asset.bestOffer
        if self.target == "Diff":
            target_value = self.asset.bestOffer - self.asset.bestBid

        logging.info("strategy:eval ", target_value, " ", self.target, " ", self.condition, " ", self.value)
            
        if self.condition == "LT" and target_value < self.value:
            self.execute(target_value)
        if self.condition == "GT" and target_value > self.value:
            self.execute(target_value)
    
    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def isRunning(self):
        return self.running

    def execute(self, target):
        ts = time.time()
        print ("Executed at ", ts)
        print ("Target Value: ", target)
        print ("Component Bid/Ask: ", str(self.asset.bestBid), "/", str(self.asset.bestOffer))
        print ("Component Values: ", self.asset.legData())
        self.tradeBroadcaster.sendFunc("Event")
        