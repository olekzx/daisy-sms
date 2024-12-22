class WrongRentalIdError(Exception):
    def __init__(self, message="Wrong rental ID"):
        self.message = message
        super().__init__(self.message)