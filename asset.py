class exchAsset:
    def __init__(self, exchange, ticker, name):
        self.exchange = exchange
        self.ticker = ticker
        self.name = name
        self.bestBid = float(0)
        self.bidSize = float(0)
        self.bestOffer = float(0)
        self.offerSize = float(0)
        
    def updateTop(self, bb, bs, bo, os):
        self.bestBid = bb
        self.bidSize = bs
        self.bestOffer = bo
        self.offerSize = os