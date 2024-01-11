from typing import List, Optional, Union

from .base import BaseMethod
from ..models.model import PersonResponse, StaffResponse
from ..exceptions import BadRequest


class Staff(BaseMethod):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._base_url = f"{self._base_url}/staff".format(api_version="v1")

    async def _by_film(self, film_id: int) -> List[StaffResponse]:
        res = await self.session._request_get(
            self._base_url, params={"filmId": film_id}
        )
        if res.status_code == 200:
            return [StaffResponse.model_validate(x) for x in res.json()]
        elif res.status_code == 404:
            return []
        else:
            raise BadRequest(res)

    async def _get_person(self, person_id: int) -> Optional[PersonResponse]:
        res = await self.session._request_get(f"{self._base_url}/{person_id}")
        if res.status_code == 200:
            return PersonResponse.model_validate(res.json())
        elif res.status_code == 404:
            return None
        else:
            raise BadRequest(res)

    async def __call__(
        self, *ignore, person_id: Optional[int] = None, film_id: Optional[int] = None
    ) -> Union[Optional[PersonResponse], List[StaffResponse]]:
        if person_id and film_id or ignore:
            raise TypeError("Must be only one arg person_id or film_id")

        if person_id:
            return await self._get_person(person_id=person_id)
        elif film_id:
            return await self._by_film(film_id=film_id)
        else:
            raise TypeError("All args are None")
