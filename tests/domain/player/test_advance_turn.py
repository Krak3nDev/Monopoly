# tests/domain/player/test_advance_turn.py

from monopoly.domain.entities.estate_state import MortgagedState, NotOwnedState


def test_advance_turn_mortgaged_state(player1, estate_clothing_not_owned):
    player1.buy_estate(estate_clothing_not_owned)
    player1.mortgage(estate_clothing_not_owned)
    initial_turns = estate_clothing_not_owned._state.turns_until_buyback
    player1.advance_turn()
    assert estate_clothing_not_owned._state.turns_until_buyback == initial_turns - 1
    assert isinstance(estate_clothing_not_owned._state, MortgagedState)

def test_advance_turn_auto_sale(player1, estate_clothing_not_owned):
    player1.buy_estate(estate_clothing_not_owned)
    player1.mortgage(estate_clothing_not_owned)

    estate_clothing_not_owned._state.turns_until_buyback = 15

    for _ in range(15):
        player1.advance_turn()

    assert estate_clothing_not_owned.owner is None

    assert isinstance(estate_clothing_not_owned._state, NotOwnedState)

    assert estate_clothing_not_owned.identity not in player1.estates