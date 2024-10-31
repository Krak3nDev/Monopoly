import logging

import betterlogging
from src.monopoly.domain.entities.estate import Estate, EstateCategory, EstateId
from src.monopoly.domain.entities.player import Player, PlayerId
from src.monopoly.domain.exceptions.base import InsufficientFundsError
from src.monopoly.domain.exceptions.estate_exc import (
    EstateAlreadyOwnedException,
    EstateNotOwnedException, TradeDifferenceExceededException, InvalidFundsException,
)
from src.monopoly.domain.value_objects.funds import Funds


def main():
    log_level = logging.INFO
    betterlogging.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    log = logging.getLogger(__name__)

    estate1 = Estate(
        identity=EstateId(1),
        name="Вулиця Медова",
        price=60,
        mortgage_price=30,
        buyback_price=33,
        category=EstateCategory.CLOTHING,
    )
    estate2 = Estate(
        identity=EstateId(2),
        name="Вулиця Балтімор",
        price=60,
        mortgage_price=30,
        buyback_price=33,
        category=EstateCategory.CLOTHING,
    )
    estates = [estate1, estate2]

    player1 = Player(identity=PlayerId(1), funds=Funds(1500))
    player2 = Player(identity=PlayerId(2), funds=Funds(1500))
    players = [player1, player2]


if __name__ == "__main__":
    main()
