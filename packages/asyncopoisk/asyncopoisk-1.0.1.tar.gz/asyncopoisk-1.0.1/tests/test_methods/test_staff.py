import pytest
from asyncopoisk import KinopoiskAPI


@pytest.mark.usefixtures("kp")
class TestStaff:
    film_id = 841700

    async def test_film_staff(self, kp: KinopoiskAPI):
        staff = await kp.staff(film_id=TestStaff.film_id)
        for person in staff:
            await kp.staff(person_id=person.staff_id)
