from asset import exchAsset
from strategy import strategy

class synthLeg:
    def __init__(self, name: str, asset: exchAsset, weight: float):
        self.name = name
        self.asset = asset
        self.weight = weight
        self.strategies = []
    
    def contribution(self, action: str):
        if (action == "BUY" and self.weight > 0):
            return float(self.weight) * float(self.asset.bestOffer)
        if (action == "SELL" and self.weight < 0):
            return float(self.weight) * -1 * float(self.asset.bestOffer)
        if action == "BUY" and self.weight < 0:
            return float(self.weight) * float(self.asset.bestBid)
        if action == "SELL" and self.weight > 0:
            return float(self.weight) * -1 * float(self.asset.bestBid)
        
class synthAsset:
    def __init__(self, assetName: str):
        self.name = assetName
        self.legs = []
        self.bestBid = 0
        self.bestOffer = 0
        self.strategies = []
        
    def addLeg(self, name: str, asset: exchAsset, weight: float):
        s = synthLeg(name, asset, weight)
        self.legs.append(s)
    
    def calcPrice(self):
        self.bestBid = self.calcPriceForAction("SELL")
        self.bestOffer = self.calcPriceForAction("BUY")
        for s in self.strategies:
            s.eval()
    
    def calcPriceForAction(self, action:str):
        return sum(map(lambda s: s.contribution(action), self.legs))
    
    def attachStrat(self, strat: strategy):
        self.strategies.append(strat)
        
    def legData(self):
        dataString: str = ""
        for s in self.legs:
            dataString += s.name + ": " + s.asset.bestBid + "/" + s.asset.bestOffer + "\n"
        return dataString
        