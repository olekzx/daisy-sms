class TooManyActiveRentalsError(Exception):
    def __init__(self, message='Too many active rentals'):
        self.message = message
        super().__init__(self.message)