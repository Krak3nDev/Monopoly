from dataclasses import dataclass, field
from enum import Enum
from typing import NewType

from src.monopoly.domain.entities.estate_state import EstateState, NotOwnedState
from src.monopoly.domain.entities.player import PlayerId

EstateId = NewType("EstateId", int)


class EstateCategory(str, Enum):
    PERFUMERY = "Perfumery"
    ELECTRONICS = "Electronics"
    AUTOMOBILES = "Automobiles"
    HOTELS = "Hotels"
    RESTAURANTS = "Restaurants"
    AIRLINES = "Airlines"
    BEVERAGES = "Beverages"
    WEB_SERVICES = "Web Services"
    CLOTHING = "Clothing"


BUILDABLE_CATEGORIES = {
    EstateCategory.PERFUMERY,
    EstateCategory.ELECTRONICS,
    EstateCategory.HOTELS,
    EstateCategory.RESTAURANTS,
    EstateCategory.AIRLINES,
    EstateCategory.BEVERAGES,
    EstateCategory.WEB_SERVICES,
    EstateCategory.CLOTHING,
}


@dataclass(kw_only=True, slots=True)
class Estate:
    identity: EstateId
    name: str
    price: int
    mortgage_price: int
    buyback_price: int
    category: EstateCategory
    _state: "EstateState" = field(default_factory=lambda: NotOwnedState())
    _owner: PlayerId | None = None

    def _set_state(self, new_state: EstateState) -> None:
        self._state = new_state

    def buy(self, player_id: PlayerId) -> None:
        self._state.buy(self, player_id)

    def mortgage(self, player_id: PlayerId) -> None:
        self._state.mortgage(self, player_id)

    def buyback(self, player_id: PlayerId) -> None:
        self._state.buyback(self, player_id)

    def advance_turn(self) -> None:
        self._state.advance_turn(self)

    @property
    def owner(self) -> PlayerId | None:
        return self._owner

    def _set_owner(self, player_id: PlayerId | None) -> None:
        self._owner = player_id


@dataclass(kw_only=True, slots=True)
class BuildableEstate(Estate):
    stars: int = 0
    max_stars: int = 5

    def build_star(self) -> None:
        if self.stars < self.max_stars:
            self.stars += 1
            print(f"Star built on {self.name}. Current stars: {self.stars}")


@dataclass(kw_only=True, slots=True)
class UnbuildableEstate(Estate):
    pass
