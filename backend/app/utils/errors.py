class AppError(Exception):
    status_code = 400
    def __init__(self, message):
        self.message = message

class AlreadyReviewedError(AppError):
    status_code = 400