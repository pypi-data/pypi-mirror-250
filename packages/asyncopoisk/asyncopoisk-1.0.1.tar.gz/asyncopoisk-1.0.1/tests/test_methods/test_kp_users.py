import pytest
from asyncopoisk import KinopoiskAPI


@pytest.mark.usefixtures("kp")
class TestKpUsers:
    user_id = 13997593

    async def test_kp_users(self, kp: KinopoiskAPI):
        await kp.kp_users.votes(user_id=TestKpUsers.user_id)

    async def test_kp_users_second_page(self, kp: KinopoiskAPI):
        await kp.kp_users.votes(user_id=TestKpUsers.user_id, page=2)
