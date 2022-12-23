class exchAsset:
    def __init__(self, exchange, ticker, name):
        self.exchange = exchange
        self.ticker = ticker
        self.name = name
        self.bestBid = float(0)
        self.bidSize = float(0)
        self.bestOffer = float(0)
        self.offerSize = float(0)
        self.synthNames = {}
        self.synths = []
        
    def updateTop(self, bb, bs, bo, os):
        self.bestBid = bb
        self.bidSize = bs
        self.bestOffer = bo
        self.offerSize = os
        
    def updateSynths(self):
        for s in self.synths:
            s.calcPrice()
            
    def addSynth(self, synthAsset):
        if synthAsset.name not in self.synthNames:
            self.synthNames.add(synthAsset.name)
            self.synths.append(synthAsset)