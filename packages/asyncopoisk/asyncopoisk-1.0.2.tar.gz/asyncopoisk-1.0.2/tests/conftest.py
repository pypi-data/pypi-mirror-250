import pytest
from _pytest.config.argparsing import Parser

from asyncopoisk import KinopoiskAPI


def pytest_addoption(parser: Parser):
    parser.addoption("--token", action="store")


def pytest_generate_tests(metafunc):
    option_value = metafunc.config.option.token
    if "token" in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("token", [option_value])


@pytest.fixture()
def kp(pytestconfig) -> KinopoiskAPI:
    return KinopoiskAPI(token=pytestconfig.getoption("token"))
