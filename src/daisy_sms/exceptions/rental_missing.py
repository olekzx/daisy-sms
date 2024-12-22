class RentalMissingError(Exception):
    def __init__(self, message="Rental missing"):
        self.message = message
        super().__init__(self.message)