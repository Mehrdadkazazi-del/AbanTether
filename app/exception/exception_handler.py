from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    def __init__(self, detail="User not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class InsufficientBalanceException(HTTPException):
    def __init__(self, detail="Insufficient balance"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class OrderNotFoundException(HTTPException):
    def __init__(self, detail="Order not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class AccountNotFoundException(HTTPException):
    def __init__(self, detail="Account not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
