import time

import pytest

from ord_mediascout_client import ORDMediascoutClient, ORDMediascoutConfig


@pytest.fixture
def client():
    config = ORDMediascoutConfig()
    return ORDMediascoutClient(config)


@pytest.fixture(scope='session', autouse=True)
def faker_session_locale():
    return ['ru_RU']


@pytest.fixture(scope='session', autouse=True)
def faker_seed():
    return int(time.time())
