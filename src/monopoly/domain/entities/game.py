import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal

from monopoly.domain.entities.estate import EstateCategory, Estate, EstateId
from monopoly.domain.entities.player import Player
from monopoly.domain.value_objects.funds import Funds

log = logging.getLogger(__name__)

category_to_estates: dict[EstateCategory, set[Estate]] = {
    category: set() for category in EstateCategory  # mypy: ignore
}

def initialize_estates():
    estates = [
        Estate(identity=EstateId(1), name="Fragrance Hub", price=100, mortgage_price=50, buyback_price=55,
               category=EstateCategory.PERFUMERY),
        Estate(identity=EstateId(2), name="Scent Station", price=110, mortgage_price=55, buyback_price=60,
               category=EstateCategory.PERFUMERY),

        Estate(identity=EstateId(3), name="Gadget World", price=150, mortgage_price=75, buyback_price=82,
               category=EstateCategory.ELECTRONICS),
        Estate(identity=EstateId(4), name="Tech Town", price=160, mortgage_price=80, buyback_price=88,
               category=EstateCategory.ELECTRONICS),

        Estate(identity=EstateId(5), name="Auto Plaza", price=200, mortgage_price=100, buyback_price=110,
               category=EstateCategory.AUTOMOBILES),
        Estate(identity=EstateId(6), name="Motor Market", price=210, mortgage_price=105, buyback_price=115,
               category=EstateCategory.AUTOMOBILES),

        Estate(identity=EstateId(7), name="Hotel California", price=300, mortgage_price=150, buyback_price=165,
               category=EstateCategory.HOTELS),
        Estate(identity=EstateId(8), name="Grand Lodge", price=320, mortgage_price=160, buyback_price=176,
               category=EstateCategory.HOTELS),

        Estate(identity=EstateId(9), name="Restaurant Royale", price=250, mortgage_price=125, buyback_price=137,
               category=EstateCategory.RESTAURANTS),
        Estate(identity=EstateId(10), name="Dine Divine", price=260, mortgage_price=130, buyback_price=143,
               category=EstateCategory.RESTAURANTS),

        Estate(identity=EstateId(11), name="Airline Terminal", price=180, mortgage_price=90, buyback_price=99,
               category=EstateCategory.AIRLINES),
        Estate(identity=EstateId(12), name="Sky Gateway", price=190, mortgage_price=95, buyback_price=105,
               category=EstateCategory.AIRLINES),

        Estate(identity=EstateId(13), name="Beverage Barn", price=120, mortgage_price=60, buyback_price=66,
               category=EstateCategory.BEVERAGES),
        Estate(identity=EstateId(14), name="Drink Depot", price=130, mortgage_price=65, buyback_price=71,
               category=EstateCategory.BEVERAGES),

        Estate(identity=EstateId(15), name="Web Services Hub", price=160, mortgage_price=80, buyback_price=88,
               category=EstateCategory.WEB_SERVICES),
        Estate(identity=EstateId(16), name="Cloud Central", price=170, mortgage_price=85, buyback_price=94,
               category=EstateCategory.WEB_SERVICES),

        Estate(identity=EstateId(17), name="Clothing Corner", price=140, mortgage_price=70, buyback_price=77,
               category=EstateCategory.CLOTHING),
        Estate(identity=EstateId(18), name="Fashion Forte", price=150, mortgage_price=75, buyback_price=83,
               category=EstateCategory.CLOTHING),
    ]

    for estate in estates:
        category_to_estates[estate.category].add(estate)

@dataclass
class Game:
    players: list[Player]
    estate_registry: dict[EstateCategory, set[Estate]]

    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime = None
    fast_mode: bool = False

    current_turn: int = 0

    pass_start_bonus: Funds = Funds(amount=2000)
    player_starting_funds: Funds = Funds(amount=2000)

    bonus_disable_after: timedelta = field(init=False)
    rent_reduction_start_after: timedelta = field(init=False)
    tax_increase_start_after: timedelta = field(init=False)

    rent_reduced: bool = field(default=False, init=False)
    tax_rate_updated: bool = field(default=False, init=False)

    rent_reduction_step: Decimal = Decimal("0.10")
    rent_reduction_interval_turns: int = 20
    max_rent_reduction: Decimal = Decimal("0.50")

    current_rent_reduction: Decimal = field(default=Decimal("0"), init=False)
    next_rent_reduction_turn: int = field(default=0, init=False)

    current_tax_rate: Decimal = Decimal("0")

    winner: Player = None

    def __post_init__(self):
        if self.fast_mode:
            self.bonus_disable_after = timedelta(minutes=31)
            self.rent_reduction_start_after = timedelta(minutes=41)
            self.tax_increase_start_after = timedelta(minutes=41)
            self.game_duration = timedelta(minutes=31)
        else:
            self.bonus_disable_after = timedelta(minutes=46)
            self.rent_reduction_start_after = timedelta(minutes=61)
            self.tax_increase_start_after = timedelta(minutes=61)
            self.game_duration = timedelta(minutes=46)

    def is_bonus_active(self) -> bool:
        elapsed_time = datetime.now() - self.start_time
        return elapsed_time < self.bonus_disable_after

    def is_rent_reduction_active(self) -> bool:
        elapsed_time = datetime.now() - self.start_time
        return elapsed_time >= self.rent_reduction_start_after

    def is_tax_increase_active(self) -> bool:
        elapsed_time = datetime.now() - self.start_time
        return elapsed_time >= self.tax_increase_start_after

    def pass_start(self, player: Player):
        if self.is_bonus_active():
            player.funds = player.funds.add(self.pass_start_bonus)
            log.info(f"Player {player.identity} passed 'Start' and receive ${self.pass_start_bonus.amount}.")
        else:
            log.info(f"Player {player.identity} passed 'Start', but the bonus was not issued (time expired).")

    def update_tax_rate(self):
        if self.is_tax_increase_active():
            if self.current_tax_rate < 0.99:
                self.current_tax_rate += 0.10
                if self.current_tax_rate > 0.99:
                    self.current_tax_rate = 0.99
                self.tax_rate_updated = True
                log.info(f"The tax rate has been increased to {self.current_tax_rate * 100}%.")


    def reduce_rent(self):
        if self.is_rent_reduction_active():
            if self.current_turn >= self.next_rent_reduction_turn and self.current_rent_reduction < self.max_rent_reduction:
                remaining_reduction = self.max_rent_reduction - self.current_rent_reduction
                reduction_step = min(self.rent_reduction_step, remaining_reduction)
                for category, estates in self.estate_registry.items():
                    for estate in estates:
                        estate.reduce_rent(percentage=reduction_step * 100)
                self.current_rent_reduction += reduction_step
                log.info(f"Rent has been reduced by {reduction_step * 100}%. Current total reduction: {self.current_rent_reduction * 100}%.")
                self.next_rent_reduction_turn = self.current_turn + self.rent_reduction_interval_turns
                if self.current_rent_reduction >= self.max_rent_reduction:
                    log.info("Maximum rent reduction reached.")


    def advance_turn(self):
        if self.winner:
            self.end_game()
            return

        self.current_turn += 1
        log.info(f"Turn {self.current_turn} begins.")

        self.update_tax_rate()
        self.reduce_rent()

        for player in self.players:
            player.advance_turn()
            # Here you can call the method for making a player's move
            # For example: player.take_turn(self)

    def end_game(self) -> Player:
        self.end_time = datetime.now()
        log.info("The game was finished")
        return self.winner

    def initialize_game(self):
        self.start_time = datetime.now()
        for player in self.players:
            player.funds = self.player_starting_funds
        log.info(f"The game started at {self.start_time}")

