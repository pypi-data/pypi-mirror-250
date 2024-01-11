from typing import Optional, List, Union

from .base import BaseMethod
from ..models.model import (
    Film,
    SeasonResponse,
    FactResponse,
    DistributionResponse,
    FilmSearchByFiltersResponse,
    BoxOfficeResponse,
    AwardResponse,
    VideoResponse,
    RelatedFilmResponse,
    ImageResponse,
    ReviewResponse,
    ExternalSourceResponse,
    FilmCollectionResponse,
    PremiereResponse,
    FiltersResponse,
    FilmSequelsAndPrequelsResponse,
    FilmSearchResponse,
    DigitalReleaseResponse,
)
from ..models.enums import (
    Order,
    ImageType,
    CollectionType,
    Month,
    SearchOrder,
    SearchFilmType,
)
from ..exceptions import BadRequest


class Films(BaseMethod):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._base_url_v1 = f"{self._base_url}/films".format(api_version="v2.1")
        self._base_url_v2 = f"{self._base_url}/films".format(api_version="v2.2")

    async def _get_film(self, film_id: int) -> Optional[Film]:
        res = await self.session._request_get(f"{self._base_url_v2}/{film_id}")
        if res.status_code == 200:
            return Film.model_validate(res.json())
        elif res.status_code == 404:
            return None
        else:
            raise BadRequest(res)

    async def _search_film(
        self,
        countries: List[int] = None,
        genres: List[int] = None,
        order: SearchOrder = SearchOrder.RATING,
        type: SearchFilmType = SearchFilmType.ALL,
        rating_from: Optional[float] = None,
        rating_to: Optional[float] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        imdb_id: Optional[str] = None,
        keyword: Optional[str] = None,
        page: Optional[int] = None,
    ) -> Optional[FilmSearchByFiltersResponse]:
        payload = {
            "countries": countries,
            "genres": genres,
            "order": order.value,
            "type": type.value,
            "ratingFrom": rating_from,
            "ratingTo": rating_to,
            "yearFrom": year_from,
            "yearTo": year_to,
            "imdbId": imdb_id,
            "keyword": keyword,
            "page": page,
        }
        payload = {k: v for k, v in payload.items() if v}

        res = await self.session._request_get(self._base_url_v2, params=payload)

        if res.status_code == 200:
            return FilmSearchByFiltersResponse.model_validate(res.json())
        elif res.status_code == 404:
            return None
        else:
            raise BadRequest(res)

    async def __call__(
        self,
        film_id: Optional[int] = None,
        countries: List[int] = None,
        genres: List[int] = None,
        order: SearchOrder = SearchOrder.RATING,
        type: SearchFilmType = SearchFilmType.ALL,
        rating_from: float = 0,
        rating_to: float = 10,
        year_from: int = 1000,
        year_to: int = 3000,
        imdb_id: Optional[str] = None,
        keyword: Optional[str] = None,
        page: int = 1,
    ) -> Optional[Union[Film, FilmSearchByFiltersResponse]]:
        if film_id:
            return await self._get_film(film_id=film_id)

        else:
            return await self._search_film(
                countries=countries,
                genres=genres,
                order=order,
                type=type,
                rating_from=rating_from,
                rating_to=rating_to,
                year_from=year_from,
                year_to=year_to,
                imdb_id=imdb_id,
                keyword=keyword,
                page=page,
            )

    async def seasons(self, film_id: int) -> SeasonResponse:
        res = await self.session._request_get(f"{self._base_url_v2}/{film_id}/seasons")
        if res.status_code == 200:
            return SeasonResponse.model_validate(res.json())
        else:
            raise BadRequest(res)

    async def facts(self, film_id: int) -> FactResponse:
        res = await self.session._request_get(f"{self._base_url_v2}/{film_id}/facts")
        if res.status_code == 200:
            return FactResponse.model_validate(res.json())
        else:
            raise BadRequest(res)

    async def distributions(self, film_id: int) -> DistributionResponse:
        res = await self.session._request_get(
            f"{self._base_url_v2}/{film_id}/distributions"
        )
        if res.status_code == 200:
            return DistributionResponse.model_validate(res.json())
        else:
            raise BadRequest(res)

    async def box_office(self, film_id: int) -> BoxOfficeResponse:
        res = await self.session._request_get(
            f"{self._base_url_v2}/{film_id}/box_office"
        )
        if res.status_code == 200:
            return BoxOfficeResponse.model_validate(res.json())
        else:
            raise BadRequest(res)

    async def awards(self, film_id: int) -> AwardResponse:
        res = await self.session._request_get(f"{self._base_url_v2}/{film_id}/awards")
        if res.status_code == 200:
            return AwardResponse.model_validate(res.json())
        else:
            raise BadRequest(res)

    async def videos(self, film_id: int) -> VideoResponse:
        res = await self.session._request_get(f"{self._base_url_v2}/{film_id}/videos")
        if res.status_code == 200:
            return VideoResponse.model_validate(res.json())
        else:
            raise BadRequest(res)

    async def similars(self, film_id: int) -> RelatedFilmResponse:
        res = await self.session._request_get(f"{self._base_url_v2}/{film_id}/similars")
        if res.status_code == 200:
            return RelatedFilmResponse.model_validate(res.json())
        else:
            raise BadRequest(res)

    async def images(
        self,
        film_id: int,
        page: int = 1,
        image_type: Optional[ImageType] = ImageType.STILL,
    ) -> ImageResponse:
        res = await self.session._request_get(
            f"{self._base_url_v2}/{film_id}/images",
            params={"page": page, "type": image_type.value},
        )
        if res.status_code == 200:
            return ImageResponse.model_validate(res.json())
        else:
            raise BadRequest(res)

    async def reviews(
        self,
        film_id: int,
        page: int = 1,
        order: Optional[Order] = Order.DATE_DESC,
    ) -> ReviewResponse:
        res = await self.session._request_get(
            f"{self._base_url_v2}/{film_id}/reviews",
            params={"page": page, "order": order.value},
        )
        if res.status_code == 200:
            return ReviewResponse.model_validate(res.json())
        else:
            raise BadRequest(res)

    async def external_sources(
        self, film_id: int, page: int = 1
    ) -> ExternalSourceResponse:
        res = await self.session._request_get(
            f"{self._base_url_v2}/{film_id}/reviews", params={"page": page}
        )
        if res.status_code == 200:
            return ExternalSourceResponse.model_validate(res.json())
        else:
            raise BadRequest(res)

    async def collections(
        self,
        page: int = 1,
        collection_type: Optional[CollectionType] = CollectionType.TOP_POPULAR_ALL,
    ) -> FilmCollectionResponse:
        res = await self.session._request_get(
            f"{self._base_url_v2}/collections",
            params={"page": page, "type": collection_type.value},
        )
        if res.status_code == 200:
            return FilmCollectionResponse.model_validate(res.json())
        else:
            raise BadRequest(res)

    async def premieres(
        self,
        year: int,
        month: Month,
    ) -> PremiereResponse:
        res = await self.session._request_get(
            f"{self._base_url_v2}/premieres",
            params={"year": year, "month": month.value},
        )
        if res.status_code == 200:
            return PremiereResponse.model_validate(res.json())
        else:
            raise BadRequest(res)

    async def filters(self) -> FiltersResponse:
        res = await self.session._request_get(f"{self._base_url_v2}/filters")
        if res.status_code == 200:
            return FiltersResponse.model_validate(res.json())
        else:
            raise BadRequest(res)

    async def sequels_and_prequels(
        self, film_id: int
    ) -> List[FilmSequelsAndPrequelsResponse]:
        res = await self.session._request_get(
            f"{self._base_url_v1}/{film_id}/sequels_and_prequels"
        )
        if res.status_code == 200:
            return [
                FilmSequelsAndPrequelsResponse.model_validate(x) for x in res.json()
            ]
        elif res.status_code == 404:
            return []
        else:
            raise BadRequest(res)

    async def search_by_keyword(
        self, keyword: str, page: int = 1
    ) -> Optional[FilmSearchResponse]:
        res = await self.session._request_get(
            f"{self._base_url_v1}/search-by-keyword",
            params={"keyword": keyword, "page": page},
        )
        if res.status_code == 200:
            return FilmSearchResponse.model_validate(res.json())
        elif res.status_code == 404:
            return None
        else:
            raise BadRequest(res)

    async def releases(
        self, year: int, month: Month, page: int = 1
    ) -> Optional[DigitalReleaseResponse]:
        res = await self.session._request_get(
            f"{self._base_url_v1}/releases",
            params={"year": year, "month": month.value, "page": page},
        )
        if res.status_code == 200:
            return DigitalReleaseResponse.model_validate(res.json())
        elif res.status_code == 404:
            return None
        else:
            raise BadRequest(res)
