from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..player import Player

@dataclass
class PlayerManager:
    players: list["Player"]

    def advance_turns(self):
        for player in self.players:
            player.advance_turn()
            # Here you can add a call to the player.take_turn(game) method
