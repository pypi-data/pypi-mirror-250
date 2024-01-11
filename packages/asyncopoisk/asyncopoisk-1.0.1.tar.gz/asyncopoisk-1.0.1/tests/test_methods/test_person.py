import pytest
from asyncopoisk import KinopoiskAPI


@pytest.mark.usefixtures("kp")
class TestPerson:
    person_name = "Мэтт"

    async def test_persons(self, kp: KinopoiskAPI):
        await kp.persons(name=TestPerson.person_name)

    async def test_persons_second_page(self, kp: KinopoiskAPI):
        await kp.persons(name=TestPerson.person_name, page=2)
