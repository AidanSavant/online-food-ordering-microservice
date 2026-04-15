from fastapi import status

class CustomerBaseException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundException(CustomerBaseException):
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)

class ValidationException(CustomerBaseException):
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

class ConflictException(CustomerBaseException):
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_409_CONFLICT)

class CustomerException(CustomerBaseException):
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)

class UnauthorizedException(CustomerBaseException):
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)

class DatabaseException(CustomerBaseException):
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InternalServerException(CustomerBaseException):
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        