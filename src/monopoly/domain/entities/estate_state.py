import logging
from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .player import PlayerId
from ..exceptions.estate_exc import EstateNotOwnedException, EstateMortgagedException, EstateAlreadyOwnedException

log = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .estate import Estate

class EstateState(ABC):
    @abstractmethod
    def buy(self, estate: 'Estate', player_id: PlayerId) -> None:
        pass

    @abstractmethod
    def mortgage(self, estate: 'Estate', player_id: PlayerId) -> None:
        pass

    @abstractmethod
    def buyback(self, estate: 'Estate', player_id: PlayerId) -> None:
        pass

    @abstractmethod
    def advance_turn(self, estate: 'Estate') -> None:
        pass

@dataclass
class NotOwnedState(EstateState):
    """
    State when the estate is not owned by any player.
    """

    def buy(self, estate: 'Estate', player_id: PlayerId) -> None:
        estate.owner = player_id
        estate.set_state(OwnedState())
        log.info(f"{estate.name} has been purchased by Player {player_id}.")

    def mortgage(self, estate: 'Estate', player_id: PlayerId) -> None:
        # Cannot mortgage an estate that is not owned
        log.error(f"Cannot mortgage {estate.name} as it is not owned.")
        raise EstateNotOwnedException(estate.name)

    def buyback(self, estate: 'Estate', player_id: PlayerId) -> None:
        # Cannot buy back an estate that is not mortgaged
        log.error(f"Cannot buyback {estate.name} as it is not mortgaged.")
        raise EstateNotOwnedException(estate.name)

    def advance_turn(self, estate: 'Estate') -> None:
        log.info(f"{estate.name} is currently 'Not Owned'. Nothing happens.")


@dataclass
class OwnedState(EstateState):
    """
    State when the estate is owned by a player.
    """

    def buy(self, estate: 'Estate', player_id: PlayerId) -> None:
        # Cannot buy an already owned estate
        log.warning(f"{estate.name} is already owned by Player {estate.owner}.")
        raise EstateAlreadyOwnedException(estate.name)

    def mortgage(self, estate: 'Estate', player_id: PlayerId) -> None:
        estate.set_state(MortgagedState(turns_until_buyback=estate.turns_until_buyback_initial))
        log.info(f"{estate.name} has been mortgaged for {estate.mortgage_price}.")

    def buyback(self, estate: 'Estate', player_id: PlayerId) -> None:
        # Cannot buy back an estate that is not mortgaged
        log.error(f"Cannot buyback {estate.name} as it is not mortgaged.")
        raise EstateMortgagedException(estate.name)

    def advance_turn(self, estate: 'Estate') -> None:
        log.info(f"{estate.name} is owned by Player {estate.owner}. Nothing happens.")



@dataclass
class MortgagedState(EstateState):
    turns_until_buyback: int = 0

    def buy(self, estate: 'Estate', player_id: PlayerId) -> None:
        raise EstateMortgagedException(estate.name)

    def mortgage(self, estate: 'Estate', player_id: PlayerId) -> None:
        log.info(f"{estate.name} is already mortgaged.")

    def buyback(self, estate: 'Estate', player_id: PlayerId) -> None:
        estate.set_state(OwnedState())
        log.info(f"{estate.name} has been bought back for {estate.buyback_price}.")

    def advance_turn(self, estate: 'Estate') -> None:
        if self.turns_until_buyback > 0:
            self.turns_until_buyback -= 1
            log.info(f"{self.turns_until_buyback} turns remaining to buy back {estate.name}.")
            if self.turns_until_buyback == 0:
                log.info(f"Time to buy back {estate.name} has expired. The estate can now be sold.")
        else:
            log.info(f"Buyback time for {estate.name} has already expired.")
