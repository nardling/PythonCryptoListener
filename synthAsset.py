from asset import exchAsset

class synthLeg:
    def __init__(self, asset: exchAsset, weight: float):
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
        
    def addLeg(self, asset: exchAsset, weight: float):
        s = synthLeg(asset, weight)
        self.legs.append(s)
        
    def getPrice(self, action:str):
        print ("In getPrice")
        return sum(map(lambda s: s.contribution(action), self.legs))
        