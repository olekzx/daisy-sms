class NotEnoughBalanceLeftError(Exception):
    def __init__(self, message='Not enough balance'):
        self.message = message
        super().__init__(self.message)