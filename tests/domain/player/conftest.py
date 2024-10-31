# tests/domain/player/conftest.py

import pytest
from monopoly.domain.entities.estate import Estate, EstateCategory, EstateId
from monopoly.domain.entities.player import Player, PlayerId
from monopoly.domain.value_objects.funds import Funds

@pytest.fixture
def estate_clothing_not_owned():
    return Estate(
        identity=EstateId(1),
        name="Honey Street",
        price=60,
        mortgage_price=30,
        buyback_price=33,
        category=EstateCategory.CLOTHING
    )

@pytest.fixture
def estate_clothing_owned():
    estate = Estate(
        identity=EstateId(2),
        name="Baltimore Street",
        price=60,
        mortgage_price=30,
        buyback_price=33,
        category=EstateCategory.CLOTHING
    )
    return estate

@pytest.fixture
def player1():
    return Player(identity=PlayerId(1), funds=Funds(amount=1500))

@pytest.fixture
def player2():
    return Player(identity=PlayerId(2), funds=Funds(amount=1500))
