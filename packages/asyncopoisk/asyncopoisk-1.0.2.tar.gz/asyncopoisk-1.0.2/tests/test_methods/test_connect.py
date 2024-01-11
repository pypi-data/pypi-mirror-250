import pytest
from asyncopoisk import KinopoiskAPI


@pytest.mark.usefixtures("kp")
class TestApiKeys:
    async def test_token(self, kp: KinopoiskAPI):
        await kp.api_keys(kp.token)
