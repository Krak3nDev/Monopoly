import logging

import betterlogging

from src.monopoly.domain.entities.estate import Estate, EstateId, EstateCategory
from src.monopoly.domain.entities.estate_state import NotOwnedState
from src.monopoly.domain.entities.player import Player, PlayerId
from src.monopoly.domain.exceptions.base import InsufficientFundsError
from src.monopoly.domain.exceptions.estate_exc import EstateNotOwnedException, EstateAlreadyOwnedException


def main():
    log_level = logging.INFO
    betterlogging.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    log = logging.getLogger(__name__)

    estate1 = Estate(identity=EstateId(1), name="Вулиця Медова", price=60, mortgage_price=30, buyback_price=33, category=EstateCategory.CLOTHING, state=NotOwnedState())
    estate2 = Estate(identity=EstateId(2), name="Вулиця Балтімор", price=60, mortgage_price=30, buyback_price=33, category=EstateCategory.CLOTHING, state=NotOwnedState())
    estates = [estate1, estate2]

    player1 = Player(identity=PlayerId(1), funds=1500)
    player2 = Player(identity=PlayerId(2), funds=1500)
    players = [player1, player2]

    for turn in range(2):
        for player in players:
            log.info(f"Player {player.identity}'s turn.")
            estate_to_buy = estates[turn]
            log.info(f"Estate available for purchase: {estate_to_buy}")

            log.info(f"Available estate: {estate_to_buy.name} for ${estate_to_buy.price}")
            try:
                player.buy_estate(estate_to_buy)
                log.info(f"Estate after purchase: {estate_to_buy}")
            except InsufficientFundsError:
                log.info(f"Player {player.identity} does not have enough funds to buy {estate_to_buy.name}")
            except EstateAlreadyOwnedException as e:
                log.info(f"Cannot buy {estate_to_buy.name}: {e}")
            except EstateNotOwnedException as e:
                log.info(f"Cannot buy {estate_to_buy.name}: {e}")

            log.info(f"Player {player.identity}'s balance: ${player.funds}")

if __name__ == "__main__":
    main()
