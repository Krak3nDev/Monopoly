import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from .player import PlayerId
from ..constants import TURNS_UNTIL_SALE
from ..exceptions.estate_exc import (
    EstateAlreadyOwnedException,
    EstateMortgagedException,
    EstateNotOwnedException, EstatePermissionException,
)

log = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .estate import Estate

class Action(str, Enum):
    BUY = "buy"
    MORTGAGE = "mortgage"
    BUYBACK = "buyback"

class EstateState(ABC):
    @abstractmethod
    def buy(self, estate: "Estate", player_id: PlayerId) -> None:
        pass

    @abstractmethod
    def mortgage(self, estate: "Estate", player_id: PlayerId) -> None:
        pass

    @abstractmethod
    def buyback(self, estate: "Estate", player_id: PlayerId) -> None:
        pass

    def advance_turn(self, estate: "Estate") -> None:
        log.info(f"Nothing happens.")



@dataclass
class NotOwnedState(EstateState):
    """
    State when the estate is not owned by any player.
    """

    def buy(self, estate: "Estate", player_id: PlayerId) -> None:
        estate._set_owner(player_id=player_id)
        estate._set_state(OwnedState())
        log.info(f"{estate.name} has been purchased by Player {player_id}.")

    def mortgage(self, estate: "Estate", player_id: PlayerId) -> None:
        # Cannot mortgage an estate that is not owned
        log.error(f"Cannot mortgage {estate.name} as it is not owned.")
        raise EstateNotOwnedException(estate.name, action=Action.MORTGAGE)

    def buyback(self, estate: "Estate", player_id: PlayerId) -> None:
        # Cannot buy back an estate that is not mortgaged
        log.error(f"Cannot buyback {estate.name} as it is not owned.")
        raise EstateNotOwnedException(estate.name, action=Action.BUYBACK)



@dataclass
class OwnedState(EstateState):
    """
    State when the estate is owned by a player.
    """

    def buy(self, estate: "Estate", player_id: PlayerId) -> None:
        # Cannot buy an already owned estate
        log.warning(f"{estate.name} is already owned by Player {estate.owner}.")
        raise EstateAlreadyOwnedException(estate.name)

    def mortgage(self, estate: "Estate", player_id: PlayerId) -> None:
        if estate.owner != player_id:
            log.error(f"Only the owner (Player {estate.owner}) can mortgage {estate.name}.")
            raise EstatePermissionException(estate.name, action=Action.MORTGAGE)

        if isinstance(estate._state, MortgagedState):
            log.error(f"{estate.name} is already mortgaged.")
            raise EstateMortgagedException(estate.name, action=Action.MORTGAGE)

        estate._set_state(MortgagedState(turns_until_buyback=TURNS_UNTIL_SALE))
        log.info(f"{estate.name} has been mortgaged for {estate.mortgage_price}.")

    def buyback(self, estate: "Estate", player_id: PlayerId) -> None:
        # Cannot buy back an estate that is not mortgaged
        log.error(f"Cannot buyback {estate.name} as it is not mortgaged.")
        raise EstateMortgagedException(estate.name, action="buy")



@dataclass
class MortgagedState(EstateState):
    turns_until_buyback: int = 0

    def buy(self, estate: "Estate", player_id: PlayerId) -> None:
        raise EstateMortgagedException(estate.name)

    def mortgage(self, estate: "Estate", player_id: PlayerId) -> None:
        log.info(f"{estate.name} is already mortgaged.")
        raise EstateMortgagedException(estate.name, action=Action.MORTGAGE)

    def buyback(self, estate: "Estate", player_id: PlayerId) -> None:
        if estate.owner != player_id:
            log.error(f"Only the owner (Player {estate.owner}) can buy back {estate.name}.")
            raise EstatePermissionException(estate.name, action=Action.BUYBACK)

        estate._set_state(OwnedState())
        log.info(f"{estate.name} has been bought back for {estate.buyback_price}.")

    def advance_turn(self, estate: "Estate") -> None:
        if self.turns_until_buyback > 0:
            self.turns_until_buyback -= 1
            log.info(f"{self.turns_until_buyback} turns remaining to buy back {estate.name}.")
            if self.turns_until_buyback == 0:
                estate._set_state(NotOwnedState())
                estate._set_owner(None)
                log.info(f"Buyback time for {estate.name} has expired. The estate is now available for purchase.")
