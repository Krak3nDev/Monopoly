import logging
from dataclasses import dataclass
from decimal import Decimal

from monopoly.domain.entities.game.time_manager import TimeManager

log = logging.getLogger(__name__)

@dataclass
class TaxManager:
    current_tax_rate: Decimal = Decimal("0")
    tax_rate_updated: bool = False
    tax_step: Decimal = Decimal("0.10")
    max_tax_rate: Decimal = Decimal("0.99")

    def update_tax_rate(self, time_manager: TimeManager):
        if (time_manager.elapsed_time() >= time_manager.tax_increase_start_after and
            not self.tax_rate_updated and
            self.current_tax_rate < self.max_tax_rate):
            self.current_tax_rate += self.tax_step
            if self.current_tax_rate > self.max_tax_rate:
                self.current_tax_rate = self.max_tax_rate
            self.tax_rate_updated = True
            log.info(f"The tax rate has been increased to {self.current_tax_rate * 100}%.")
