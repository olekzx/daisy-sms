class NoNumbersLeftError(Exception):
    def __init__(self, message="No numbers left"):
        self.message = message
        super().__init__(self.message)
