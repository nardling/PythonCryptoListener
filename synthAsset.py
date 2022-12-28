from asset import exchAsset

class synthLeg:
    def __init__(self, name: str, asset: exchAsset, weight: float):
        self.name = name
        self.asset = asset
        self.weight = weight
    
    def contribution(self, action: str):
        print (self.asset)
        print (self.asset.name, self.asset.bestBid, self.weight)
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
        
    def addLeg(self, name: str, asset: exchAsset, weight: float):
        s = synthLeg(name, asset, weight)
        self.legs.append(s)
    
    def calcPrice(self):
        self.bestBid = self.calcPriceForAction("SELL")
        self.bestOffer = self.calcPriceForAction("BUY")
    
    def calcPriceForAction(self, action:str):
        return sum(map(lambda s: s.contribution(action), self.legs))
        