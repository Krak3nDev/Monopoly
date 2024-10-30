import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, NewType

from src.monopoly.domain.exceptions.base import InsufficientFundsError
from src.monopoly.domain.exceptions.estate_exc import EstateAlreadyOwnedException

if TYPE_CHECKING:
    from src.monopoly.domain.entities.estate import Estate

log = logging.getLogger(__name__)


PlayerId = NewType("PlayerId", int)


@dataclass(kw_only=True, slots=True)
class Player:
    identity: PlayerId
    funds: int = 15000

    def buy_estate(self, estate: "Estate") -> None:
        if self.funds >= estate.price:
            try:
                estate.buy(player_id=self.identity)
                self.funds -= estate.price
                log.info(f"Player {self.identity} successfully bought {estate.name}")
            except EstateAlreadyOwnedException as e:
                log.info(f"Unable to buy {estate.name}: {e}")
        else:
            raise InsufficientFundsError(
                f"Player {self.identity} does not have enough funds to purchase {estate.name}"
            )
