import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, NewType

from src.monopoly.domain.exceptions.base import InsufficientFundsError

if TYPE_CHECKING:
    from src.monopoly.domain.entities.estate import Estate

log = logging.getLogger(__name__)


PlayerId = NewType("PlayerId", int)


@dataclass(kw_only=True, slots=True)
class Player:
    identity: PlayerId
    funds: int = 15000
    estates: list["Estate"] = field(default_factory=list)

    def buy_estate(self, estate: "Estate") -> None:
        if self.funds >= estate.price:
            estate.buy(player_id=self.identity)
            self.funds -= estate.price
            self.estates.append(estate)
            log.info(f"Player {self.identity} successfully bought {estate.name}")
        else:
            log.error(
                f"Player {self.identity} does not have enough funds to purchase {estate.name}."
            )
            raise InsufficientFundsError(
                f"Player {self.identity} does not have enough funds to purchase {estate.name}."
            )

    def mortgage(self, estate: "Estate"):
        self.funds += estate.mortgage_price
        estate.mortgage(player_id=self.identity)
        log.info(f"Player {self.identity} successfully mortgaged {estate.name}")

    def buyback(self, estate: "Estate"):
        if self.funds >= estate.buyback_price:
            self.funds -= estate.buyback_price
            estate.buyback(player_id=self.identity)
            log.info(f"Player {self.identity} successfully buybacked {estate.name}")

    def advance_turn(self):
        for estate in self.estates:
            estate.advance_turn()

