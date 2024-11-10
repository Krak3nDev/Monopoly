from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..estate import Estate, EstateCategory

@dataclass
class EstateManager:
    estate_registry: dict["EstateCategory", set["Estate"]]

    def reduce_all_rents(self, percentage: float):
        for category, estates in self.estate_registry.items():
            for estate in estates:
                estate.reduce_rent(percentage=percentage)
