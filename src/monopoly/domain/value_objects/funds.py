from dataclasses import dataclass
from functools import total_ordering

from src.monopoly.domain.exceptions.estate_exc import InvalidFundsException

@dataclass(frozen=True, order=True)
class Funds:
    amount: int = 15000

    def __post_init__(self):
        if self.amount < 0:
            raise InvalidFundsException(amount=self.amount)

    def add(self, other: 'Funds') -> 'Funds':
        return Funds(amount=self.amount + other.amount)

    def subtract(self, other: 'Funds') -> 'Funds':
        if self.amount < other.amount:
            raise InvalidFundsException(amount=other.amount, action="subtract")
        return Funds(amount=self.amount - other.amount)

    def __str__(self):
        return f"${self.amount}"

