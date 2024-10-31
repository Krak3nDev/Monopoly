# tests/domain/player/test_mortgage.py

import pytest

from monopoly.domain.entities.estate_state import MortgagedState, NotOwnedState
from monopoly.domain.exceptions.estate_exc import EstateNotOwnedException, EstateMortgagedException

def test_mortgage_estate_success(player1, estate_clothing_not_owned):
    # Player 1 buys the estate
    player1.buy_estate(estate_clothing_not_owned)
    # Player 1 mortgages the estate
    player1.mortgage(estate_clothing_not_owned)
    assert isinstance(estate_clothing_not_owned._state, MortgagedState)
    assert estate_clothing_not_owned.owner == player1.identity
    assert estate_clothing_not_owned.identity in player1.estates
    assert player1.funds.amount == 1500 - 60 + 30  # Purchase price + mortgage amount

def test_mortgage_estate_not_owned(player1, estate_clothing_not_owned):
    # Player 1 attempts to mortgage a property they do not own
    with pytest.raises(EstateNotOwnedException):
        player1.mortgage(estate_clothing_not_owned)
    assert isinstance(estate_clothing_not_owned._state, NotOwnedState)
    assert estate_clothing_not_owned.owner is None
    assert estate_clothing_not_owned.identity not in player1.estates
    assert player1.funds.amount == 1500

def test_mortgage_estate_already_mortgaged(player1, estate_clothing_not_owned):
    # Player 1 buys and mortgages the estate
    player1.buy_estate(estate_clothing_not_owned)
    player1.mortgage(estate_clothing_not_owned)
    # Attempt to mortgage an already mortgaged estate
    with pytest.raises(EstateMortgagedException):
        player1.mortgage(estate_clothing_not_owned)
    assert isinstance(estate_clothing_not_owned._state, MortgagedState)
    assert estate_clothing_not_owned.owner == player1.identity
    assert estate_clothing_not_owned.identity in player1.estates
    assert player1.funds.amount == 1500 - 60 + 30
