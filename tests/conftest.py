import logging

import betterlogging
import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    log_level = logging.INFO
    betterlogging.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger()
    logger.setLevel(log_level)

    yield