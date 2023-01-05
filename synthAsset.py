from asset import exchAsset
from strategy import strategy

class synthLeg:
    def __init__(self, name: str, asset: exchAsset, weight: float):
        self.name = name
        self.asset = asset
        self.weight = weight
        self.strategies = []
        self.mdTime = 0
    
    def contribution(self, action: str):
        if (action == "BUY" and self.weight > 0):
            return float(self.weight) * float(self.asset.bestOffer)
        if (action == "SELL" and self.weight < 0):
            return float(self.weight) * -1 * float(self.asset.bestOffer)
        if action == "BUY" and self.weight < 0:
            return float(self.weight) * float(self.asset.bestBid)
        if action == "SELL" and self.weight > 0:
            return float(self.weight) * -1 * float(self.asset.bestBid)

    def size(self, action: str):
        if (action == "BUY" and self.weight > 0):
            return float(self.asset.offerSize)
        if (action == "SELL" and self.weight < 0):
            return float(self.asset.offerSize)
        if action == "BUY" and self.weight < 0:
            return float(self.asset.bidSize)
        if action == "SELL" and self.weight > 0:
            return float(self.asset.bidSize)

    def legTradeDetail(self, action: str):
        if (action == "BUY" and self.weight > 0):
            return float(self.asset.bestOffer), "BUY"
        if (action == "SELL" and self.weight < 0):
            return float(self.asset.bestOffer), "BUY"
        if action == "BUY" and self.weight < 0:
            return float(self.asset.bestBid), "SELL"
        if action == "SELL" and self.weight > 0:
            return float(self.asset.bestBid), "SELL"

    def getState(self):
        return self.asset.getState()
        
class synthAsset:
    def __init__(self, assetName: str):
        self.name = assetName
        self.legs = []
        self.bestBid = 0
        self.bestOffer = 0
        self.bidSize = 0
        self.askSize = 0
        self.strategies = []
        
    def addLeg(self, name: str, asset: exchAsset, weight: float):
        s = synthLeg(name, asset, weight)
        self.legs.append(s)
    
    def calcPrice(self):
        self.bestBid = self.calcPriceForAction("SELL")
        self.bestOffer = self.calcPriceForAction("BUY")
        self.bidSize = self.calcSizeForAction("SELL")
        self.offerSize = self.calcSizeForAction("BUY")
        for s in self.strategies:
            s.eval()
    
    def calcSizeForAction(self, action: str):
        return min(map(lambda s: s.size(action), self.legs))

    def calcPriceForAction(self, action:str):
        return sum(map(lambda s: s.contribution(action), self.legs))
    
    def attachStrat(self, strat: strategy):
        self.strategies.append(strat)
        
    def legData(self, action: str):
        legData = []
        for s in self.legs:
            p, a = s.legTradeDetail(action)
            legData.append({"asset_name": s.asset.name, "exec_price": p, "trade_action": a})
        return legData

    def getState(self):
        legState = []
        for s in self.legs:
            legState.append(s.getState())
        return legState
        