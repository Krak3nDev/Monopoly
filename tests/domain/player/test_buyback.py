# tests/domain/player/test_buyback.py

import pytest

from monopoly.domain.entities.estate_state import OwnedState, MortgagedState
from monopoly.domain.exceptions.estate_exc import EstateMortgagedException
from monopoly.domain.exceptions.base import InsufficientFundsError
from monopoly.domain.value_objects.funds import Funds


def test_buyback_estate_success(player1, estate_clothing_not_owned):
    # Player 1 buys and mortgages the property
    player1.buy_estate(estate_clothing_not_owned)
    player1.mortgage(estate_clothing_not_owned)
    # Player 1 buys back the mortgage
    player1.buyback(estate_clothing_not_owned)
    assert isinstance(estate_clothing_not_owned._state, OwnedState)
    assert estate_clothing_not_owned.owner == player1.identity
    assert estate_clothing_not_owned.identity in player1.estates
    assert player1.funds.amount == 1500 - 60 + 30 - 33  # Purchase price + mortgage - buyback

def test_buyback_estate_not_mortgaged(player1, estate_clothing_not_owned):
    # Player 1 buys the property but does not mortgage it
    player1.buy_estate(estate_clothing_not_owned)
    with pytest.raises(EstateMortgagedException):
        player1.buyback(estate_clothing_not_owned)
    assert isinstance(estate_clothing_not_owned._state, OwnedState)
    assert estate_clothing_not_owned.owner == player1.identity
    assert estate_clothing_not_owned.identity in player1.estates
    assert player1.funds.amount == 1500 - 60

def test_buyback_estate_insufficient_funds(player1, estate_clothing_not_owned):
    # Player 1 buys and mortgages the property
    player1.buy_estate(estate_clothing_not_owned)
    player1.mortgage(estate_clothing_not_owned)
    # Reduce the player's balance to an amount insufficient for buyback
    player1.funds = Funds(amount=10)
    with pytest.raises(InsufficientFundsError):
        player1.buyback(estate_clothing_not_owned)
    assert isinstance(estate_clothing_not_owned._state, MortgagedState)
    assert estate_clothing_not_owned.owner == player1.identity
    assert estate_clothing_not_owned.identity in player1.estates
    assert player1.funds.amount == 10
