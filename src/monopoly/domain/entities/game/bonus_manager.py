from dataclasses import dataclass
from decimal import Decimal
import logging

from monopoly.domain.entities.game.time_manager import TimeManager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..player import Player


log = logging.getLogger(__name__)

@dataclass
class BonusManager:
    pass_start_bonus: Decimal = Decimal("2000")
    player_starting_funds: Decimal = Decimal("2000")

    def pass_start(self, player: "Player", time_manager: TimeManager):
        if time_manager.elapsed_time() < time_manager.bonus_disable_after:
            player.funds += self.pass_start_bonus
            log.info(
                f"Player {player.identity} passed 'Start' and received ${self.pass_start_bonus}.")
        else:
            log.info(
                f"Player {player.identity} passed 'Start', but the bonus was not issued (time expired).")
