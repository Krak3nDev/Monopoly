import logging
from dataclasses import dataclass
from typing import NewType, TYPE_CHECKING

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

    def buy_estate(self, estate: 'Estate') -> None:
        if self.funds >= estate.price:
            try:
                estate.buy(player_id=self.identity)
                self.funds -= estate.price
                log.info(f"Гравець {self.identity} успішно купив {estate.name}")
            except EstateAlreadyOwnedException as e:
                log.info(f"Не можна купити {estate.name}: {e}")
        else:
            raise InsufficientFundsError(f"У Гравця {self.identity} недостатньо коштів для покупки {estate.name}")
