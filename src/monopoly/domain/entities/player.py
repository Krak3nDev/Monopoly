import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, NewType

from src.monopoly.domain.exceptions.base import InsufficientFundsError
from src.monopoly.domain.exceptions.estate_exc import TradeDifferenceExceededException, EstateNotOwnedException
from src.monopoly.domain.value_objects.funds import Funds

if TYPE_CHECKING:
    from src.monopoly.domain.entities.estate import Estate

log = logging.getLogger(__name__)


PlayerId = NewType("PlayerId", int)


@dataclass(kw_only=True, slots=True)
class Player:
    identity: PlayerId
    funds: Funds
    estates: list["Estate"] = field(default_factory=list)

    def buy_estate(self, estate: "Estate") -> None:
        if self.funds.amount >= estate.price:
            estate.buy(player_id=self.identity)
            self.funds = self.funds.subtract(Funds(amount=estate.price))
            self.estates.append(estate)
            log.info(f"Player {self.identity} successfully bought {estate.name}")
        else:
            log.error(
                f"Player {self.identity} does not have enough funds to purchase {estate.name}."
            )
            raise InsufficientFundsError(
                f"Player {self.identity} does not have enough funds to purchase {estate.name}."
            )

    def mortgage(self, estate: "Estate"):
        self.funds = self.funds.add(other=Funds(amount=estate.mortgage_price))
        estate.mortgage(player_id=self.identity)
        log.info(f"Player {self.identity} successfully mortgaged {estate.name}")

    def buyback(self, estate: "Estate"):
        if self.funds.amount >= estate.buyback_price:
            self.funds = self.funds.subtract(other=Funds(amount=estate.buyback_price))
            estate.buyback(player_id=self.identity)
            log.info(f"Player {self.identity} successfully buybacked {estate.name}")

    def advance_turn(self):
        for estate in self.estates:
            estate.advance_turn()

    def trade_estates(
        self,
        other_player: "Player",
        estates_to_give: list["Estate"],
        estates_to_receive: list["Estate"],
        funds_to_give: Funds = Funds(amount=0),
        funds_to_receive: Funds = Funds(amount=0),
    ) -> None:
        """
        Trades estates and/or funds with another player.
        :param other_player: The player to trade with.
        :param estates_to_give: List of estates to give to the other player.
        :param estates_to_receive: List of estates to receive from the other player.
        :param funds_to_give: Amount of funds to give to the other player.
        :param funds_to_receive: Amount of funds to receive from the other player.
        :raises EstateNotOwnedException: If trying to trade estates not owned.
        :raises EstateAlreadyOwnedException: If receiving an estate already owned.
        :raises InsufficientFundsError: If not enough funds to give.
        :raises TradeDifferenceExceededException: If trade difference exceeds 50%.
        """
        total_given = sum(estate.price for estate in estates_to_give) + funds_to_give.amount
        total_received = sum(estate.price for estate in estates_to_receive) + funds_to_receive.amount

        log.debug(f"Player {self.identity} is attempting to trade.")
        log.debug(f"Total given: ${total_given}, Total received: ${total_received}")

        if total_given > 2 * total_received or total_received > 2 * total_given:
            raise TradeDifferenceExceededException(
                player_id=self.identity,
                given=total_given,
                received=total_received
            )

        for estate in estates_to_give:
            if estate.owner != self.identity:
                raise EstateNotOwnedException(estate.name, action="trade")

        for estate in estates_to_receive:
            if estate.owner != other_player.identity:
                raise EstateNotOwnedException(estate.name, action="trade")

        if self.funds < funds_to_give:
            raise InsufficientFundsError(f"Player {self.identity} does not have enough funds to give.")
        if self.funds < funds_to_receive:
            raise InsufficientFundsError(f"Player {other_player.identity} does not have enough funds to give.")

        try:
            self.funds = self.funds.subtract(other=funds_to_give)
            other_player.funds = other_player.funds.add(other=funds_to_give)
            log.info(f"Player {self.identity} gave ${funds_to_give} to Player {other_player.identity}.")

            other_player.funds = other_player.funds.subtract(other=funds_to_receive)
            self.funds = self.funds.add(other=funds_to_receive)
            log.info(f"Player {other_player.identity} gave ${funds_to_receive} to Player {self.identity}.")

            for estate in estates_to_give:
                self.estates.remove(estate)
                estate._set_owner(other_player.identity)
                other_player.estates.append(estate)
                log.info(f"Player {self.identity} traded estate '{estate.name}' to Player {other_player.identity}.")

            for estate in estates_to_receive:
                other_player.estates.remove(estate)
                estate._set_owner(self.identity)
                self.estates.append(estate)
                log.info(f"Player {other_player.identity} traded estate '{estate.name}' to Player {self.identity}.")

        except Exception as e:
            log.error(f"Trade failed: {e}")
            raise

