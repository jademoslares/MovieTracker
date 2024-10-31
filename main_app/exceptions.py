class MovieNotFoundException(Exception):
    def __init__(self, message="Movie not found"):
        self.message = message
        super().__init__(self.message)


class FormNotValidException(Exception):
    def __init__(self, message="Form is not valid"):
        self.message = message
        super().__init__(self.message)

class UserNotAuthorizedException(Exception):
    def __init__(self, message="User not authorized"):
        self.message = message
        super().__init__(self.message)