class strategy:
    def __init__(self, asset, target, condition, value, action):
        self.asset = asset
        self.target = target
        self.condition = condition
        self.value = value
        self.action = action
            
    def eval(self):
        target_value = 0
        
        if self.target == "Buy":
            target_value = self.asset.bestBid
        if self.target == "Sell":
            target_value = self.asset.bestOffer
        if self.target == "Diff":
            target_value = self.asset.bestOffer - self.asset.bestBid
            
        if self.condition == "LT" and target_value < self.value:
            print("Perform Action")
        if self.condition == "GT" and target_value > self.value:
            print("Perform Action")