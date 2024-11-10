from dataclasses import dataclass, field
from decimal import Decimal
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..estate import Estate, EstateCategory


log = logging.getLogger(__name__)

@dataclass
class RentManager:
    rent_reduction_step: Decimal = Decimal("0.10")
    rent_reduction_interval_turns: int = 20
    max_rent_reduction: Decimal = Decimal("0.50")
    current_rent_reduction: Decimal = Decimal("0")
    next_rent_reduction_turn: int = field(default=20)

    def reduce_rent(self, current_turn: int, estate_registry: dict["EstateCategory", set["Estate"]]):
        if (current_turn >= self.next_rent_reduction_turn and
            self.current_rent_reduction < self.max_rent_reduction):
            remaining_reduction = self.max_rent_reduction - self.current_rent_reduction
            reduction_step = min(self.rent_reduction_step, remaining_reduction)
            for category, estates in estate_registry.items():
                for estate in estates:
                    estate.reduce_rent(percentage=reduction_step * 100)
            self.current_rent_reduction += reduction_step
            log.info(
                f"Rent has been reduced by {reduction_step * 100}%. "
                f"Current total reduction: {self.current_rent_reduction * 100}%.")
            self.next_rent_reduction_turn += self.rent_reduction_interval_turns
            if self.current_rent_reduction >= self.max_rent_reduction:
                log.info("Maximum rent reduction reached.")
