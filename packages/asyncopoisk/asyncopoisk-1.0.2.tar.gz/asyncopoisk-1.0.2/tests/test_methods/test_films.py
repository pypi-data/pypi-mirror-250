import pytest
from asyncopoisk import KinopoiskAPI
from asyncopoisk.models.enums import Month, Order, CollectionType


@pytest.mark.usefixtures("kp")
class TestFilms:
    film_id = 841700
    imdb_id = "tt3659388"

    async def test_search_by_film_id(self, kp: KinopoiskAPI):
        await kp.films(film_id=TestFilms.film_id)

    async def test_search_genres_filter(self, kp: KinopoiskAPI):
        await kp.films(genres=[11])

    async def test_search_by_imdb_id(self, kp: KinopoiskAPI):
        await kp.films(imdb_id=TestFilms.imdb_id)

    async def test_empty_filter(self, kp: KinopoiskAPI):
        await kp.films()

    async def test_empty_filter_second_page(self, kp: KinopoiskAPI):
        await kp.films(page=2)

    async def test_seasons(self, kp: KinopoiskAPI):
        await kp.films.seasons(TestFilms.film_id)

    async def test_facts(self, kp: KinopoiskAPI):
        await kp.films.facts(TestFilms.film_id)

    async def test_distributions(self, kp: KinopoiskAPI):
        await kp.films.distributions(TestFilms.film_id)

    async def test_box_office(self, kp: KinopoiskAPI):
        await kp.films.box_office(TestFilms.film_id)

    async def test_awards(self, kp: KinopoiskAPI):
        await kp.films.awards(TestFilms.film_id)

    async def test_videos(self, kp: KinopoiskAPI):
        await kp.films.videos(TestFilms.film_id)

    async def test_similars(self, kp: KinopoiskAPI):
        await kp.films.similars(TestFilms.film_id)

    async def test_images(self, kp: KinopoiskAPI):
        await kp.films.images(TestFilms.film_id)

    async def test_reviews(self, kp: KinopoiskAPI):
        await kp.films.reviews(TestFilms.film_id)

    async def test_reviews_order(self, kp: KinopoiskAPI):
        await kp.films.reviews(TestFilms.film_id, order=Order.DATE_ASC)

    async def test_reviews_second_page(self, kp: KinopoiskAPI):
        await kp.films.reviews(TestFilms.film_id, page=2)

    async def test_external_sources(self, kp: KinopoiskAPI):
        await kp.films.external_sources(TestFilms.film_id)

    async def test_external_sources_second_page(self, kp: KinopoiskAPI):
        await kp.films.external_sources(TestFilms.film_id, page=2)

    async def test_collections(self, kp: KinopoiskAPI):
        await kp.films.collections()

    async def test_collections_second_page(self, kp: KinopoiskAPI):
        await kp.films.collections(page=2)

    async def test_collections_type(self, kp: KinopoiskAPI):
        await kp.films.collections(collection_type=CollectionType.FAMILY)

    async def test_premieres(self, kp: KinopoiskAPI):
        await kp.films.premieres(2023, month=Month.APRIL)

    async def test_premieres_future(self, kp: KinopoiskAPI):
        await kp.films.premieres(3000, month=Month.APRIL)

    async def test_filters(self, kp: KinopoiskAPI):
        await kp.films.filters()

    async def test_sequels_and_prequels(self, kp: KinopoiskAPI):
        await kp.films.sequels_and_prequels(TestFilms.film_id)

    async def test_search_by_keyword(self, kp: KinopoiskAPI):
        await kp.films.search_by_keyword("Матрица")

    async def test_releases(self, kp: KinopoiskAPI):
        await kp.films.releases(2023, Month.APRIL)
