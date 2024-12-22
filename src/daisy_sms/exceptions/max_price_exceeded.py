class MaxPriceExceededError(Exception):
    def __init__(self, message="Max price exceeded"):
        self.message = message
        super().__init__(self.message)
