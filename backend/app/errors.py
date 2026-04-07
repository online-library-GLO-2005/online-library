# Mainly for all Errors that we have
class AppError(Exception):
    def __init__(self, status_code: int, message: str, is_operational: bool = True):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.is_operational = is_operational
