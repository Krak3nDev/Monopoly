from .base import DomainError

class EstateNotOwnedException(DomainError):
    def __init__(self, estate_name: str, action: str = "perform the action"):
        self.message = f"Estate '{estate_name}' is not owned. Cannot {action}."
        super().__init__(self.message)

class EstateMortgagedException(DomainError):
    def __init__(self, estate_name: str, action: str = "perform the action"):
        self.message = f"Estate '{estate_name}' is mortgaged. Cannot {action}."
        super().__init__(self.message)


class MaxStarsReachedException(DomainError):
    def __init__(self, estate_name: str, max_stars: int):
        self.message = (
            f"Cannot add more stars to '{estate_name}'. "
            f"Maximum number of stars ({max_stars}) reached."
        )
        super().__init__(self.message)


class EstateAlreadyOwnedException(DomainError):
    def __init__(self, estate_name: str):
        self.message = f"Estate '{estate_name}' is already owned by another player."
        super().__init__(self.message)

class EstatePermissionException(DomainError):
    def __init__(self, estate_name: str, action: str = "perform the action"):
        self.message = f"Cannot {action} '{estate_name}': permission denied."
        super().__init__(self.message)


class TradeDifferenceExceededException(DomainError):
    def __init__(self, player_id: int, given: int, received: int):
        self.message = (
            f"Trade difference exceeded for Player {player_id}. "
            f"Given: ${given}, Received: ${received}. "
            f"Trade must not exceed a 50% difference."
        )
        super().__init__(self.message)


class InvalidFundsException(DomainError):
    def __init__(self, amount: int, action: str = "perform the action"):
        self.message = f"Invalid funds amount: {amount}. Cannot {action}."
        super().__init__(self.message)

class TradeMustIncludeAtLeastOneEstateException(DomainError):
    def __init__(self):
        self.message = "Trade must include at least one estate."
        super().__init__(self.message)
