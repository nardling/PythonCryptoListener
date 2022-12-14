class exchAsset:
    def __init__(self, exchange, ticker, name):
        self.exchange = exchange
        self.ticker = ticker
        self.name = name
        self.bestBid = 0
        self.bidSize = 0
        self.bestOffer = 0
        self.offerSize = 0
        
    def updateTop(self, bb, bs, bo, os):
        self.bestBid = bb
        self.bidSize = bs
        self.bestOffer = bo
        self.offerSize = os