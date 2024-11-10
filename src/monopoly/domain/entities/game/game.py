import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING

from monopoly.domain.entities.game.bonus_manager import BonusManager
from monopoly.domain.entities.game.estate_manager import EstateManager
from monopoly.domain.entities.game.player_manager import PlayerManager
from monopoly.domain.entities.game.rent_manager import RentManager
from monopoly.domain.entities.game.tax_manager import TaxManager
from monopoly.domain.entities.game.time_manager import TimeManager

if TYPE_CHECKING:
    from ..estate import EstateCategory, Estate
    from ..player import Player

log = logging.getLogger(__name__)

@dataclass
class Game:
    players: list["Player"]
    estate_registry: dict["EstateCategory", set["Estate"]]
    fast_mode: bool = False

    time_manager: TimeManager = field(init=False)
    tax_manager: TaxManager = field(init=False)
    rent_manager: RentManager = field(init=False)
    bonus_manager: BonusManager = field(init=False)
    player_manager: PlayerManager = field(init=False)
    estate_manager: EstateManager = field(init=False)

    current_turn: int = 0
    winner: "Player" | None = None

    def __post_init__(self):
        self.time_manager = TimeManager(fast_mode=self.fast_mode)
        self.tax_manager = TaxManager()
        self.rent_manager = RentManager()
        self.bonus_manager = BonusManager()
        self.player_manager = PlayerManager(players=self.players)
        self.estate_manager = EstateManager(estate_registry=self.estate_registry)

        self.rent_manager.next_rent_reduction_turn = self.rent_manager.rent_reduction_interval_turns

    def initialize_game(self):
        self.time_manager.start_time = datetime.now()
        for player in self.players:
            player.funds = self.bonus_manager.player_starting_funds
        log.info(f"The game started at {self.time_manager.start_time}.")

    def start_game(self):
        self.initialize_game()

    def advance_turn(self):
        if self.winner:
            self.end_game()
            return

        self.current_turn += 1
        log.info(f"Turn {self.current_turn} begins.")

        self.tax_manager.update_tax_rate(self.time_manager)

        self.rent_manager.reduce_rent(self.current_turn, self.estate_registry)

        self.player_manager.advance_turns()

        if self.time_manager.is_game_over():
            self.end_game()

    def is_game_over(self) -> bool:
        return self.time_manager.is_game_over()

    def end_game(self):
        self.time_manager.end_game()
        log.info("The game has ended.")
        self.winner = self.get_winner()

    def get_winner(self) -> "Player":
        winner = max(self.players, key=lambda p: p.funds)
        log.info(f"The winner is Player {winner.identity} with ${winner.funds}.")
        self.winner = winner
        return winner