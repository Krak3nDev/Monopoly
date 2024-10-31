import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, NewType

from monopoly.domain.exceptions.base import InsufficientFundsError
from monopoly.domain.exceptions.estate_exc import TradeDifferenceExceededException, EstateNotOwnedException
from monopoly.domain.value_objects.funds import Funds

if TYPE_CHECKING:
    from monopoly.domain.entities.estate import Estate, EstateId

log = logging.getLogger(__name__)


PlayerId = NewType("PlayerId", int)


@dataclass(kw_only=True, slots=True)
class Player:
    identity: PlayerId
    funds: Funds
    estates: dict["EstateId", "Estate"] = field(default_factory=dict)

    def _add_estate(self, estate: "Estate") -> None:
        estate_id = estate.identity
        self.estates[estate_id] = estate
        estate.set_owner(self.identity)
        log.info(f"Estate '{estate.name}' added to Player {self.identity}'s estates.")

    def _remove_estate(self, estate: "Estate") -> None:
        estate_id = estate.identity
        if estate_id in self.estates:
            del self.estates[estate_id]
            estate.set_owner(None)
            log.info(f"Estate '{estate.name}' removed from Player {self.identity}'s estates.")
        else:
            log.error(f"Player {self.identity} does not own estate '{estate.name}' and cannot remove it.")
            raise EstateNotOwnedException(f"Player {self.identity} does not own estate '{estate.name}'.")

    def buy_estate(self, estate: "Estate") -> None:
        if self.funds.amount >= estate.price:
            estate.buy(player_id=self.identity)
            self.funds = self.funds.subtract(Funds(amount=estate.price))
            self._add_estate(estate)
            log.info(f"Player {self.identity} successfully bought {estate.name}")
        else:
            log.error(
                f"Player {self.identity} does not have enough funds to purchase {estate.name}."
            )
            raise InsufficientFundsError(
                f"Player {self.identity} does not have enough funds to purchase {estate.name}."
            )

    def mortgage(self, estate: "Estate"):
        estate.mortgage(player_id=self.identity)
        self.funds = self.funds.add(other=Funds(amount=estate.mortgage_price))
        log.info(f"Player {self.identity} successfully mortgaged {estate.name}")

    def buyback(self, estate: "Estate"):
        if self.funds.amount < estate.buyback_price:
            log.info(f"Cannot buy back {estate.name}: Not enough funds.")
            raise InsufficientFundsError(f"Player {self.identity} does not have enough funds to buy back {estate.name}.")

        estate.buyback(player_id=self.identity)

        self.funds = self.funds.subtract(other=Funds(amount=estate.buyback_price))
        log.info(f"Player {self.identity} successfully buybacked {estate.name}")

    def advance_turn(self):
        for estate in self.estates.values():
            estate.advance_turn()

        self.estates = {estate_id: estate for estate_id, estate in self.estates.items() if estate.owner == self.identity}

        log.info(f"Player {self.identity} estates after advance_turn: {[estate.name for estate in self.estates.values()]}")

    def trade_estates(
        self,
        other_player: "Player",
        estates_to_give: list["Estate"],
        estates_to_receive: list["Estate"],
        funds_to_give: Funds = Funds(amount=0),
        funds_to_receive: Funds = Funds(amount=0),
    ) -> None:
        total_given = sum(estate.price for estate in estates_to_give) + funds_to_give.amount
        total_received = sum(estate.price for estate in estates_to_receive) + funds_to_receive.amount

        log.debug(f"Player {self.identity} is attempting to trade with Player {other_player.identity}.")
        log.debug(f"Total given: ${total_given}, Total received: ${total_received}")

        if total_given > 2 * total_received or total_received > 2 * total_given:
            raise TradeDifferenceExceededException(
                player_id=self.identity,
                given=total_given,
                received=total_received
            )

        for estate in estates_to_give:
            estate_id = estate.identity
            if estate_id not in self.estates:
                log.error(f"Player {self.identity} does not own estate '{estate.name}' and cannot trade it.")
                raise EstateNotOwnedException(estate.name, action="trade")

        for estate in estates_to_receive:
            estate_id = estate.identity
            if estate_id not in other_player.estates:
                log.error(f"Player {other_player.identity} does not own estate '{estate.name}' and cannot trade it.")
                raise EstateNotOwnedException(estate.name, action="trade")

        if self.funds.amount < funds_to_give.amount:
            log.error(f"Player {self.identity} does not have enough funds to give ${funds_to_give.amount}.")
            raise InsufficientFundsError(f"Player {self.identity} does not have enough funds to give ${funds_to_give.amount}.")
        if other_player.funds.amount < funds_to_receive.amount:
            log.error(f"Player {other_player.identity} does not have enough funds to give ${funds_to_receive.amount}.")
            raise InsufficientFundsError(f"Player {other_player.identity} does not have enough funds to give ${funds_to_receive.amount}.")

        try:
            if funds_to_give.amount > 0:
                self.funds = self.funds.subtract(funds_to_give)
                other_player.funds = other_player.funds.add(funds_to_give)
                log.info(f"Player {self.identity} gave ${funds_to_give.amount} to Player {other_player.identity}.")

            if funds_to_receive.amount > 0:
                other_player.funds = other_player.funds.subtract(funds_to_receive)
                self.funds = self.funds.add(funds_to_receive)
                log.info(f"Player {other_player.identity} gave ${funds_to_receive.amount} to Player {self.identity}.")

            for estate in estates_to_give:
                self._remove_estate(estate)
                other_player._add_estate(estate)
                log.info(f"Player {self.identity} traded estate '{estate.name}' to Player {other_player.identity}.")

            for estate in estates_to_receive:
                other_player._remove_estate(estate)
                self._add_estate(estate)
                log.info(f"Player {other_player.identity} traded estate '{estate.name}' to Player {self.identity}.")

        except Exception as e:
            log.error(f"Trade failed: {e}")
            raise
