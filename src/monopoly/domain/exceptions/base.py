class DomainError(Exception):
    pass


class InsufficientFundsError(DomainError):
    def __init__(self, message="There are insufficient funds for the purchase of the enterprise"):
        super().__init__(message)
