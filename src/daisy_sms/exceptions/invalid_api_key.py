class InvalidApiKeyError(Exception):
    def __init__(self, message="Invalid API key"):
        self.message = message
        super().__init__(self.message)