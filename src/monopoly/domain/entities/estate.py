from dataclasses import dataclass
from enum import Enum
from typing import NewType

from src.monopoly.domain.entities.estate_state import EstateState
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
    EstateCategory.CLOTHING
}

@dataclass(kw_only=True, slots=True)
class Estate:
    identity: EstateId
    name: str
    price: int
    mortgage_price: int
    buyback_price: int
    category: EstateCategory
    state: EstateState
    owner: PlayerId | None = None
    turns_until_buyback_initial: int = 0

    def set_state(self, new_state: EstateState) -> None:
        self.state = new_state

    def buy(self, player_id: PlayerId) -> None:
        self.state.buy(self, player_id)

    def mortgage(self, player_id: PlayerId) -> None:
        self.state.mortgage(self, player_id)

    def buyback(self, player_id: PlayerId) -> None:
        self.state.buyback(self, player_id)

    def advance_turn(self) -> None:
        self.state.advance_turn(self)


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

