from asset import exchAsset
from time import time

class strategy:
    def __init__(self, asset: exchAsset, target: str, condition: str, value: float, action: str):
        self.asset = asset
        self.target = target
        self.condition = condition
        self.value = value
        self.action = action
        self.lastTradeTime = 0
            
    def eval(self):
        target_value = 0
        
        if self.target == "Buy":
            target_value = self.asset.bestBid
        if self.target == "Sell":
            target_value = self.asset.bestOffer
        if self.target == "Diff":
            target_value = self.asset.bestOffer - self.asset.bestBid
            
        if self.condition == "LT" and target_value < self.value:
            self.execute()
        if self.condition == "GT" and target_value > self.value:
            self.execute()
    
    def execute(self, target):
        ts = time.time()
        print ("Executed at ", ts)
        print ("Target Value: ", target)
        print ("Component Bid/Ask: ", self.asset.bestBid, "/", self.asset.bestOffer)
        print ("Component Values: ", self.asset.legData())
        