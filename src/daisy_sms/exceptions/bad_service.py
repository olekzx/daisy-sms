class BadServiceError(Exception):
    def __init__(self, message='Bad service'):
        self.message = message
        super().__init__(self.message)
