from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class TimeManager:
    fast_mode: bool = False
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime | None = None
    game_duration: timedelta = field(init=False)

    bonus_disable_after: timedelta = field(init=False)
    rent_reduction_start_after: timedelta = field(init=False)
    tax_increase_start_after: timedelta = field(init=False)

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

    def elapsed_time(self) -> timedelta:
        return datetime.now() - self.start_time

    def is_game_over(self) -> bool:
        return bool(self.end_time)

    def end_game(self):
        self.end_time = datetime.now()