from .base import DomainError


class EstateNotOwnedException(DomainError):
    """Exception raised when attempting to build a star on an unowned estate."""

    def __init__(self, estate_name: str):
        self.message = f"Estate '{estate_name}' is not owned. Cannot build a star."
        super().__init__(self.message)


class EstateMortgagedException(DomainError):
    """Exception raised when attempting to build a star on a mortgaged estate."""

    def __init__(self, estate_name: str):
        self.message = f"Estate '{estate_name}' is mortgaged. Cannot build a star."
        super().__init__(self.message)


class MaxStarsReachedException(DomainError):
    """Exception raised when the maximum number of stars on an estate has been reached."""

    def __init__(self, estate_name: str, max_stars: int):
        self.message = (f"Cannot build a star on '{estate_name}'. "
                        f"Maximum number of stars ({max_stars}) reached.")
        super().__init__(self.message)


class EstateAlreadyOwnedException(Exception):
    def __init__(self, estate_name: str):
        super().__init__(f"Estate '{estate_name}' is already owned by another player.")
