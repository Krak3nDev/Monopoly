import pytest

from monopoly.domain.exceptions.base import InsufficientFundsError
from monopoly.domain.exceptions.estate_exc import EstateAlreadyOwnedException
from monopoly.domain.value_objects.funds import Funds


def test_buy_estate_success(player1, estate_clothing_not_owned):
    # Player 1 buys estate that does not belong to anyone
    player1.buy_estate(estate_clothing_not_owned)
    assert estate_clothing_not_owned.owner == player1.identity
    assert estate_clothing_not_owned.identity in player1.estates
    assert player1.funds.amount == 1500 - estate_clothing_not_owned.price

def test_buy_estate_insufficient_funds(player1, estate_clothing_not_owned):
    # We reduce the player's balance to 50, which is not enough to buy real estate
    player1.funds = Funds(amount=50)
    with pytest.raises(InsufficientFundsError):
        player1.buy_estate(estate_clothing_not_owned)
    assert estate_clothing_not_owned.owner is None
    assert estate_clothing_not_owned.identity not in player1.estates
    assert player1.funds.amount == 50

def test_buy_estate_already_owned(player1, player2, estate_clothing_owned):
    # Player 1 buys real estate
    player1.buy_estate(estate_clothing_owned)
    # Player 2 tries to buy the same property
    with pytest.raises(EstateAlreadyOwnedException):
        player2.buy_estate(estate_clothing_owned)
    assert estate_clothing_owned.owner == player1.identity
    assert estate_clothing_owned.identity in player1.estates
    assert estate_clothing_owned.identity not in player2.estates
    assert player2.funds.amount == 1500
