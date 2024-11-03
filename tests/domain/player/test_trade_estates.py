# tests/domain/player/test_trade_estates.py
import pytest

from monopoly.domain.exceptions.base import InsufficientFundsError
from monopoly.domain.exceptions.estate_exc import TradeDifferenceExceededException, EstateNotOwnedException, \
    TradeMustIncludeAtLeastOneEstateException
from monopoly.domain.value_objects.funds import Funds


def test_trade_estates_success(player1, player2, estate_clothing_owned, estate_clothing_not_owned):
    """
    Test that two players can successfully trade estates and funds.
    """
    player1.buy_estate(estate_clothing_owned)
    player2.buy_estate(estate_clothing_not_owned)

    assert estate_clothing_owned.identity in player1.estates
    assert estate_clothing_not_owned.identity in player2.estates

    funds_to_give = Funds(amount=100)
    funds_to_receive = Funds(amount=80)

    player1.trade_estates(
        other_player=player2,
        estates_to_give=[estate_clothing_owned],
        estates_to_receive=[estate_clothing_not_owned],
        funds_to_give=funds_to_give,
        funds_to_receive=funds_to_receive
    )

    assert estate_clothing_owned.owner == player2.identity
    assert estate_clothing_not_owned.owner == player1.identity
    assert estate_clothing_owned.identity in player2.estates
    assert estate_clothing_not_owned.identity in player1.estates
    assert estate_clothing_owned.identity not in player1.estates
    assert estate_clothing_not_owned.identity not in player2.estates

    expected_player1_funds = 1500 - estate_clothing_owned.price - funds_to_give.amount + funds_to_receive.amount
    expected_player2_funds = 1500 - estate_clothing_not_owned.price - funds_to_receive.amount + funds_to_give.amount
    assert player1.funds.amount == expected_player1_funds
    assert player2.funds.amount == expected_player2_funds

def test_trade_estates_trade_difference_exceeded(player1, player2, estate_clothing_owned, estate_clothing_not_owned):
    """
    Test that a trade exceeding 50% difference in total given and received raises an exception.
    """
    player1.buy_estate(estate_clothing_owned)
    player2.buy_estate(estate_clothing_not_owned)

    funds_to_give = Funds(amount=200)
    funds_to_receive = Funds(amount=50)

    with pytest.raises(TradeDifferenceExceededException):
        player1.trade_estates(
            other_player=player2,
            estates_to_give=[estate_clothing_owned],
            estates_to_receive=[estate_clothing_not_owned],
            funds_to_give=funds_to_give,
            funds_to_receive=funds_to_receive
        )

def test_trade_estates_estate_not_owned(player1, player2, estate_clothing_not_owned):
    """
    Test that a player cannot trade an estate they do not own.
    """
    player2.buy_estate(estate_clothing_not_owned)

    with pytest.raises(EstateNotOwnedException):
        player1.trade_estates(
            other_player=player2,
            estates_to_give=[estate_clothing_not_owned],
            estates_to_receive=[],
            funds_to_give=Funds(amount=0),
            funds_to_receive=Funds(amount=0)
        )

def test_trade_estates_insufficient_funds(player1, player2, estate_clothing_owned, estate_clothing_not_owned):
    """
    Test that a trade where a player does not have enough funds raises an exception.
    """
    player1.buy_estate(estate_clothing_owned)
    player2.buy_estate(estate_clothing_not_owned)

    funds_to_give = Funds(amount=1450)
    funds_to_receive = Funds(amount=750)

    with pytest.raises(InsufficientFundsError):
        player1.trade_estates(
            other_player=player2,
            estates_to_give=[estate_clothing_owned],
            estates_to_receive=[estate_clothing_not_owned],
            funds_to_give=funds_to_give,
            funds_to_receive=funds_to_receive
        )

def test_trade_estates_only_funds_invalid(player1, player2):
    """
    Test that trading only funds without any estates raises an exception.
    """

    funds_to_give = Funds(amount=100)
    funds_to_receive = Funds(amount=80)

    with pytest.raises(TradeMustIncludeAtLeastOneEstateException):
        player1.trade_estates(
            other_player=player2,
            estates_to_give=[],
            estates_to_receive=[],
            funds_to_give=funds_to_give,
            funds_to_receive=funds_to_receive
        )
