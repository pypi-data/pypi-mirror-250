from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, model_serializer, field_validator

from .enums import (
    ProductionStatus,
    FilmType,
    FactType,
    DistributionType,
    ReleaseType,
    RelationType,
    ProfessionKey,
    Sex,
    AccountType,
    RelationType1,
    ReviewType,
    Site,
)


def to_camel(string: str) -> str:
    first, *others = string.split("_")
    return "".join([first.lower(), *map(str.title, others)])


class Base(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)


class Fact(Base):
    text: str = Field(
        ...,
        examples=[
            "В эпизоде, где Тринити и Нео в поисках Морфиуса оказываются на крыше..."
        ],
    )
    type: FactType = Field(..., examples=["BLOOPER"])
    spoiler: bool = Field(..., examples=[False])


class BoxOffice(Base):
    type: str = Field(..., examples=["BUDGET"])
    amount: int = Field(..., examples=[63000000])
    currency_code: str = Field(..., examples=["USD"])
    name: str = Field(..., examples=["US Dollar"])
    symbol: str = Field(..., examples=["$"])


class AwardPerson(Base):
    kinopoisk_id: int = Field(
        ...,
        examples=[1937039],
    )
    web_url: str = Field(
        ...,
        examples=["https://www.kinopoisk.ru/name/1937039/"],
    )
    name_ru: Optional[str] = Field(..., examples=["Джон Т. Рейц"])
    name_en: Optional[str] = Field(..., examples=["John T. Reitz"])
    sex: str = Field(..., examples=["MALE"])
    poster_url: str = Field(
        ...,
        examples=[
            "https://kinopoiskapiunofficial.tech/images/actor_posters/kp/1937039.jpg"
        ],
    )
    growth: Optional[int] = Field(..., examples=[178])
    birthday: Optional[str] = Field(..., examples=["1955-11-02"])
    death: Optional[str] = Field(..., examples=["2019-01-06"])
    age: Optional[int] = Field(..., examples=[21])
    birthplace: Optional[str] = Field(..., examples=["Лос-Анджелес, Калифорния, США"])
    deathplace: Optional[str] = Field(..., examples=["Лос-Анджелес, Калифорния, США"])
    profession: Optional[str] = Field(..., examples=["Монтажер, Продюсер"])


class Company(Base):
    name: str = Field(..., examples=["Каро-Премьер"])

    @model_serializer
    def ser_model(self) -> str:
        return self.name


class Episode(Base):
    season_number: int = Field(..., examples=[1])
    episode_number: int = Field(..., examples=[1])
    name_ru: Optional[str] = Field(
        ..., examples=["Глава первая: Исчезновение Уилла Байерса"]
    )
    name_en: Optional[str] = Field(
        ...,
        examples=["Chapter One: The Vanishing of Will Byers"],
    )
    synopsis: Optional[str] = Field(..., examples=["The Vanishing of Will Byers..."])
    releaseDate: Optional[str] = Field(..., examples=["2016-07-15"])


class Country(Base):
    country: str = Field(..., examples=["США"])

    @model_serializer
    def ser_model(self) -> str:
        return self.country


class Genre(Base):
    genre: str = Field(..., examples=["фантастика"])

    @model_serializer
    def ser_model(self) -> str:
        return self.genre


class FilmSequelsAndPrequelsResponse(Base):
    film_id: int = Field(
        ...,
        examples=[301],
    )
    name_ru: str = Field(..., examples=["Матрица"])
    name_en: str = Field(..., examples=["The Matrix"])
    name_original: str = Field(..., examples=["The Matrix"])
    poster_url: str = Field(
        ..., examples=["https://kinopoiskapiunofficial.tech/images/posters/kp/301.jpg"]
    )
    poster_url_preview: str = Field(
        ...,
        examples=[
            "https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg"
        ],
    )
    relation_type: RelationType = Field(..., examples=["SEQUEL"])


class StaffResponse(Base):
    staff_id: int = Field(
        ...,
        examples=[66539],
    )
    name_ru: Optional[str] = Field(..., examples=["Винс Гиллиган"])
    name_en: Optional[str] = Field(..., examples=["Vince Gilligan"])
    description: Optional[str] = Field(..., examples=["Neo"])
    poster_url: str = Field(
        ..., examples=["https://st.kp.yandex.net/images/actor/66539.jpg"]
    )
    profession_text: str = Field(..., examples=["Режиссеры"])
    profession_key: ProfessionKey = Field(
        ...,
        examples=["DIRECTOR"],
    )


class PremiereResponseItem(Base):
    kinopoisk_id: int = Field(
        ...,
        examples=[301],
    )
    name_ru: Optional[str] = Field(
        ...,
        examples=["Дитя погоды"],
    )
    name_en: Optional[str] = Field(
        ...,
        examples=["Tenki no ko"],
    )
    year: int = Field(..., examples=[2019])
    poster_url: str = Field(
        ...,
        examples=["http://kinopoiskapiunofficial.tech/images/posters/kp/1219417.jpg"],
    )
    poster_url_preview: str = Field(
        ...,
        examples=[
            "https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg"
        ],
    )
    countries: List[Country]
    genres: List[Genre]
    duration: Optional[int] = Field(..., examples=[112])
    premiere_ru: str = Field(..., examples=["2020-06-01"])


class DigitalReleaseItem(Base):
    film_id: int = Field(
        ...,
        examples=[301],
    )
    name_ru: Optional[str] = Field(..., examples=["Дитя погоды"])
    name_en: Optional[str] = Field(..., examples=["Tenki no ko"])
    year: Optional[int] = Field(..., examples=[2019])
    poster_url: str = Field(
        ...,
        examples=["http://kinopoiskapiunofficial.tech/images/posters/kp/1219417.jpg"],
    )
    poster_url_preview: str = Field(
        ...,
        examples=[
            "https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg"
        ],
    )
    countries: List[Country]
    genres: List[Genre]
    rating: Optional[float] = Field(..., examples=[7.962])
    rating_vote_count: Optional[int] = Field(..., examples=[14502])
    expectations_rating: Optional[float] = Field(..., examples=[99.13])
    expectations_rating_vote_count: Optional[int] = Field(..., examples=[1123])
    duration: Optional[int] = Field(..., examples=[112])
    release_date: str = Field(..., examples=["2020-06-01"])


class ApiError(Base):
    message: str = Field(..., examples=["User test@test.ru is inactive or deleted."])

    @model_serializer
    def ser_model(self) -> str:
        return self.message


class FiltersResponseGenres(Base):
    id: Optional[int] = Field(None, examples=[1])
    genre: Optional[str] = Field(None, examples=["боевик"])


class FiltersResponseCountries(Base):
    id: Optional[int] = Field(None, examples=[1])
    country: Optional[str] = Field(None, examples=["США"])


class FilmSearchResponseFilms(Base):
    film_id: Optional[int] = Field(None, examples=[263531])
    name_ru: Optional[str] = Field(None, examples=["Мстители"])
    name_en: Optional[str] = Field(None, examples=["The Avengers"])
    type: Optional[FilmType] = Field(None, examples=["FILM"])
    year: Optional[int] = Field(None, examples=[2012])
    description: Optional[str] = Field(None, examples=["США, Джосс Уидон(фантастика)"])
    film_length: Optional[str] = Field(None, examples=["2:17"])
    countries: Optional[List[Country]] = None
    genres: Optional[List[Genre]] = None
    rating: Optional[str] = Field(
        None,
        examples=["NOTE!!! 7.9 for released film or 99% if film have not released yet"],
    )
    rating_vote_count: Optional[int] = Field(None, examples=[284245])
    poster_url: Optional[str] = Field(
        None,
        examples=["http://kinopoiskapiunofficial.tech/images/posters/kp/263531.jpg"],
    )
    poster_url_preview: Optional[str] = Field(
        None,
        examples=[
            "https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg"
        ],
    )

    @field_validator("year", mode="before")
    def year_field_validator(cls, v: Optional[Union[str, int]]) -> Optional[int]:
        if v == "null":
            return None

        try:
            return int(v)
        except ValueError:
            raise ValueError("year must be `null` or int")

    @field_validator("rating", mode="before")
    def rating_validator(cls, v: Optional[Union[str, int]]) -> Optional[int]:
        if v == "null":
            return None

        return str(v)


class FilmSearchByFiltersResponseItems(Base):
    kinopoisk_id: Optional[int] = Field(None, examples=[263531])
    imdb_id: Optional[str] = Field(None, examples=["tt0050561"])
    name_ru: Optional[str] = Field(
        None,
        examples=["Мстители"],
    )
    name_en: Optional[str] = Field(None, examples=["The Avengers"])
    name_original: Optional[str] = Field(
        None,
        examples=["The Avengers"],
    )
    countries: Optional[List[Country]] = None
    genres: Optional[List[Genre]] = None
    rating_kinopoisk: Optional[float] = Field(
        None,
        examples=[7.9],
    )
    rating_imdb: Optional[float] = Field(None, examples=[7.9])
    year: Optional[float] = Field(None, examples=[2012])
    type: Optional[FilmType] = Field(None, examples=["FILM"])
    poster_url: Optional[str] = Field(
        None,
        examples=["http://kinopoiskapiunofficial.tech/images/posters/kp/263531.jpg"],
    )
    poster_url_preview: Optional[str] = Field(
        None,
        examples=[
            "https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg"
        ],
    )


class RelatedFilmResponseItems(Base):
    film_id: Optional[int] = Field(None, examples=[301])
    name_ru: Optional[str] = Field(None, examples=["Матрица"])
    name_en: Optional[str] = Field(None, examples=["The Matrix"])
    name_original: Optional[str] = Field(None, examples=["The Matrix"])
    poster_url: Optional[str] = Field(
        None, examples=["https://kinopoiskapiunofficial.tech/images/posters/kp/301.jpg"]
    )
    poster_url_preview: Optional[str] = Field(
        None,
        examples=[
            "https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg"
        ],
    )
    relation_type: Optional[RelationType1] = Field(None, examples=["SIMILAR"])


class ReviewResponseItems(Base):
    kinopoisk_id: Optional[int] = Field(None, examples=[2])
    type: Optional[ReviewType] = None
    date: Optional[str] = Field(None, examples=["2010-09-05T20:37:00"])
    positive_rating: Optional[int] = Field(None, examples=[122])
    negative_rating: Optional[int] = Field(None, examples=[12])
    author: Optional[str] = Field(None, examples=["Username"])
    title: Optional[str] = Field(None, examples=["Title"])
    description: Optional[str] = Field(None, examples=["text"])


class ExternalSourceResponseItems(Base):
    url: Optional[str] = Field(
        None,
        examples=[
            "https://okko.tv/movie/equilibrium?utm_medium=referral&utm_source=yandex_search&utm_campaign=new_search_feed"
        ],
    )
    platform: Optional[str] = Field(None, examples=["Okko"])
    logo_url: Optional[str] = Field(
        None,
        examples=[
            "https://avatars.mds.yandex.net/get-ott/239697/7713e586-17d1-42d1-ac62-53e9ef1e70c3/orig"
        ],
    )
    positive_rating: Optional[int] = Field(None, examples=[122])
    negative_rating: Optional[int] = Field(None, examples=[12])
    author: Optional[str] = Field(None, examples=["Username"])
    title: Optional[str] = Field(None, examples=["Title"])
    description: Optional[str] = Field(None, examples=["text"])


class FilmCollectionResponseItems(Base):
    kinopoisk_id: Optional[int] = Field(None, examples=[263531])
    name_ru: Optional[str] = Field(None, examples=["Мстители"])
    name_en: Optional[str] = Field(None, examples=["The Avengers"])
    name_original: Optional[str] = Field(None, examples=["The Avengers"])
    countries: Optional[List[Country]] = None
    genres: Optional[List[Genre]] = None
    rating_kinopoisk: Optional[float] = Field(None, examples=[7.9])
    rating_imbd: Optional[float] = Field(None, examples=[7.9])
    year: Optional[int] = Field(None, examples=[2012])
    type: Optional[FilmType] = Field(None, examples=["FILM"])
    poster_url: Optional[str] = Field(
        None,
        examples=["http://kinopoiskapiunofficial.tech/images/posters/kp/263531.jpg"],
    )
    poster_url_preview: Optional[str] = Field(
        None,
        examples=[
            "https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg"
        ],
    )


class PersonResponseSpouses(Base):
    person_id: Optional[int] = Field(None, examples=[32169])
    name: Optional[str] = Field(None, examples=["Сьюзан Дауни"])
    divorced: Optional[bool] = Field(None, examples=[False])
    divorced_reason: Optional[str] = Field(None, examples=[""])
    sex: Optional[Sex] = Field(None, examples=["MALE"])
    children: Optional[int] = Field(None, examples=[2])
    web_url: Optional[str] = Field(
        None, examples=["https://www.kinopoisk.ru/name/32169/"]
    )
    relation: Optional[str] = Field(None, examples=["супруга"])


class PersonResponseFilms(Base):
    film_id: Optional[int] = Field(None, examples=[32169])
    name_ru: Optional[str] = Field(None, examples=["Солист"])
    name_en: Optional[str] = Field(None, examples=["The Soloist"])
    rating: Optional[str] = Field(
        None, examples=["7.2 or 76% if film has not released yet"]
    )
    general: Optional[bool] = Field(None, examples=[False])
    description: Optional[str] = Field(None, examples=["Steve Lopez"])
    profession_key: Optional[ProfessionKey] = Field(None, examples=["ACTOR"])


class PersonByNameResponseItems(Base):
    kinopoisk_id: Optional[int] = Field(None, examples=[66539])
    web_url: Optional[str] = Field(None, examples=["10096"])
    name_ru: Optional[str] = Field(None, examples=["Винс Гиллиган"])
    name_en: Optional[str] = Field(None, examples=["Vince Gilligan"])
    sex: Optional[Sex] = Field(None, examples=["MALE"])
    poster_url: Optional[str] = Field(
        None,
        examples=[
            "https://kinopoiskapiunofficial.tech/images/actor_posters/kp/10096.jpg"
        ],
    )


class ImageResponseItems(Base):
    image_url: Optional[str] = Field(
        None,
        examples=[
            "https://avatars.mds.yandex.net/get-kinopoisk-image/4303601/2924f6c4-4ea0-4a1d-9a48-f29577172b27/orig"
        ],
    )
    preview_url: Optional[str] = Field(
        None,
        examples=[
            "https://avatars.mds.yandex.net/get-kinopoisk-image/4303601/2924f6c4-4ea0-4a1d-9a48-f29577172b27/300x"
        ],
    )


class VideoResponseItems(Base):
    url: Optional[str] = Field(
        None, examples=["https://www.youtube.com/watch?v=gbcVZgO4n4E"]
    )
    name: Optional[str] = Field(
        None, examples=["Мстители: Финал – официальный трейлер (16+)"]
    )
    site: Optional[Site] = Field(None, examples=["YOUTUBE"])


class KinopoiskUserVoteResponseItems(Base):
    kinopoisk_id: Optional[int] = Field(None, examples=[263531])
    name_ru: Optional[str] = Field(None, examples=["Мстители"])
    name_en: Optional[str] = Field(None, examples=["The Avengers"])
    name_original: Optional[str] = Field(None, examples=["The Avengers"])
    countries: Optional[List[Country]] = None
    genres: Optional[List[Genre]] = None
    rating_kinopoisk: Optional[float] = Field(None, examples=[7.9])
    rating_imbd: Optional[float] = Field(None, examples=[7.9])
    year: Optional[int] = Field(None, examples=[2012])
    type: Optional[FilmType] = Field(None, examples=["FILM"])
    poster_url: Optional[str] = Field(
        None,
        examples=["http://kinopoiskapiunofficial.tech/images/posters/kp/263531.jpg"],
    )
    poster_url_preview: Optional[str] = Field(
        None,
        examples=[
            "https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg"
        ],
    )
    user_rating: Optional[int] = Field(
        None,
        examples=[7],
    )

    @field_validator("year", mode="before")
    def year_field_validator(cls, v: Optional[Union[str, int]]) -> Optional[int]:
        if v == "null":
            return None

        try:
            return int(v)
        except ValueError:
            raise ValueError("year must be `null` or int")


class ApiKeyResponseTotalQuota(Base):
    value: int = Field(..., examples=[1000])
    used: int = Field(..., examples=[2])


class ApiKeyResponseDailyQuota(Base):
    value: int = Field(..., examples=[500])
    used: int = Field(..., examples=[2])


class Film(Base):
    kinopoisk_id: int = Field(..., examples=[301])
    kinopoisk_hd_id: Optional[str] = Field(
        ..., examples=["4824a95e60a7db7e86f14137516ba590"], alias="kinopoiskHDId"
    )
    imdb_id: Optional[str] = Field(..., examples=["tt0133093"])
    name_ru: Optional[str] = Field(..., examples=["Матрица"])
    name_en: Optional[str] = Field(..., examples=["The Matrix"])
    name_original: Optional[str] = Field(..., examples=["The Matrix"])
    poster_url: str = Field(
        ..., examples=["https://kinopoiskapiunofficial.tech/images/posters/kp/301.jpg"]
    )
    poster_url_preview: str = Field(
        ...,
        examples=[
            "https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg"
        ],
    )
    cover_url: Optional[str] = Field(
        ...,
        examples=[
            "https://avatars.mds.yandex.net/get-ott/1672343/2a0000016cc7177239d4025185c488b1bf43/orig"
        ],
    )
    logo_url: Optional[str] = Field(
        ...,
        examples=[
            "https://avatars.mds.yandex.net/get-ott/1648503/2a00000170a5418408119bc802b53a03007b/orig"
        ],
    )
    reviews_count: int = Field(..., examples=[293])
    rating_good_review: Optional[float] = Field(..., examples=[88.9])
    rating_good_review_vote_count: Optional[int] = Field(..., examples=[257])
    rating_kinopoisk: Optional[float] = Field(..., examples=[8.5])
    rating_kinopoisk_vote_count: Optional[int] = Field(..., examples=[524108])
    rating_imdb: Optional[float] = Field(..., examples=[8.7])
    rating_imdb_vote_count: Optional[int] = Field(..., examples=[1729087])
    rating_film_critics: Optional[float] = Field(..., examples=[7.8])
    rating_film_critics_vote_count: Optional[int] = Field(..., examples=[155])
    rating_await: Optional[float] = Field(..., examples=[7.8])
    rating_await_count: Optional[int] = Field(..., examples=[2])
    rating_rf_critics: Optional[float] = Field(
        ...,
        examples=[7.8],
    )
    rating_rf_critics_vote_count: Optional[int] = Field(..., examples=[31])
    web_url: str = Field(..., examples=["https://www.kinopoisk.ru/film/301/"])
    year: Optional[int] = Field(..., examples=[1999])
    film_length: Optional[int] = Field(..., examples=[136])
    slogan: Optional[str] = Field(..., examples=["Добро пожаловать в реальный мир"])
    description: Optional[str] = Field(
        ..., examples=["Жизнь Томаса Андерсона разделена на\xa0две части:"]
    )
    short_description: Optional[str] = Field(
        ...,
        examples=[
            "Хакер Нео узнает, что его мир — виртуальный. Выдающийся экшен, доказавший, что зрелищное кино может быть умным"
        ],
    )
    editor_annotation: Optional[str] = Field(
        ..., examples=["Фильм доступен только на языке оригинала с русскими субтитрами"]
    )
    is_tickets_available: bool = Field(..., examples=[False])
    production_status: Optional[ProductionStatus] = Field(
        ..., examples=["POST_PRODUCTION"]
    )
    type: FilmType = Field(..., examples=["FILM"])
    rating_mpaa: Optional[str] = Field(..., examples=["r"])
    rating_age_limits: Optional[str] = Field(..., examples=["age16"])
    has_imax: Optional[bool] = Field(..., examples=[False])
    has_3d: Optional[bool] = Field(..., examples=[False])
    last_sync: str = Field(..., examples=["2021-07-29T20:07:49.109817"])
    countries: List[Country]
    genres: List[Genre]
    start_year: Optional[int] = Field(..., examples=[1996])
    end_year: Optional[int] = Field(..., examples=[1996])
    serial: Optional[bool] = Field(None, examples=[False])
    short_film: Optional[bool] = Field(None, examples=[False])
    completed: Optional[bool] = Field(None, examples=[False])


class FactResponse(Base):
    total: int = Field(..., examples=[5])
    items: List[Fact]


class BoxOfficeResponse(Base):
    total: int = Field(..., examples=[5])
    items: List[BoxOffice]


class Award(Base):
    name: str = Field(..., examples=["Оскар"])
    win: bool = Field(..., examples=[True])
    image_url: Optional[str] = Field(
        ...,
        examples=[
            "https://avatars.mds.yandex.net/get-kinopoisk-image/1600647/09035193-2458-4de7-a7df-ad8f85b73798/orig"
        ],
    )
    nomination_name: str = Field(..., examples=["Лучший звук"])
    year: int = Field(..., examples=[2000])
    persons: Optional[List[AwardPerson]] = None


class Distribution(Base):
    type: DistributionType = Field(..., examples=["PREMIERE"])
    sub_type: Optional[ReleaseType] = Field(..., examples=["CINEMA"])
    date: Optional[str] = Field(..., examples=["1999-05-07"])
    re_release: Optional[bool] = Field(..., examples=[False])
    country: Optional[Country]
    companies: List[Company]


class Season(Base):
    number: int = Field(..., examples=[1])
    episodes: List[Episode]


class FiltersResponse(Base):
    genres: List[FiltersResponseGenres]
    countries: List[FiltersResponseCountries]


class FilmSearchResponse(Base):
    keyword: str = Field(..., examples=["мстители"])
    pages_count: int = Field(..., examples=[7])
    search_films_count_result: int = Field(
        ...,
        examples=[134],
    )
    films: List[FilmSearchResponseFilms]


class FilmSearchByFiltersResponse(Base):
    total: int = Field(..., examples=[7])
    total_pages: int = Field(..., examples=[1])
    items: List[FilmSearchByFiltersResponseItems]


class RelatedFilmResponse(Base):
    total: int = Field(..., examples=[7])
    items: List[RelatedFilmResponseItems]


class ReviewResponse(Base):
    total: int = Field(
        ..., description="Суммарное кол-во пользовательских рецензий", examples=[12]
    )
    total_pages: int = Field(..., examples=[2])
    total_positive_reviews: int = Field(..., examples=[1])
    total_negative_reviews: int = Field(..., examples=[7])
    total_neutral_reviews: int = Field(..., examples=[12])
    items: List[ReviewResponseItems]


class ExternalSourceResponse(Base):
    total: int = Field(..., description="Суммарное кол-во сайтов", examples=[12])
    items: List[ExternalSourceResponseItems]


class FilmCollectionResponse(Base):
    total: int = Field(..., examples=[200])
    total_pages: int = Field(..., examples=[7])
    items: List[FilmCollectionResponseItems]


class PersonResponse(Base):
    person_id: int = Field(
        ...,
        examples=[66539],
    )
    web_url: Optional[str] = Field(..., examples=["10096"])
    name_ru: Optional[str] = Field(..., examples=["Винс Гиллиган"])
    name_en: Optional[str] = Field(..., examples=["Vince Gilligan"])
    sex: Optional[Sex] = Field(..., examples=["MALE"])
    poster_url: str = Field(
        ...,
        examples=[
            "https://kinopoiskapiunofficial.tech/images/actor_posters/kp/10096.jpg"
        ],
    )
    growth: Optional[int] = Field(..., examples=["174"])
    birthday: Optional[str] = Field(..., examples=["1965-04-04"])
    death: Optional[str] = Field(..., examples=["2008-01-22"])
    age: Optional[int] = Field(..., examples=[55])
    birthplace: Optional[str] = Field(..., examples=["Манхэттэн, Нью-Йорк, США"])
    deathplace: Optional[str] = Field(..., examples=["Манхэттэн, Нью-Йорк, США"])
    has_awards: Optional[int] = Field(..., examples=[1])
    profession: Optional[str] = Field(..., examples=["Актер, Продюсер, Сценарист"])
    facts: List[str]
    spouses: List[PersonResponseSpouses]
    films: List[PersonResponseFilms]


class PersonByNameResponse(Base):
    total: int = Field(..., examples=[35])
    items: List[PersonByNameResponseItems]


class ImageResponse(Base):
    total: int = Field(..., description="Общее кол-во изображений", examples=[50])
    total_pages: int = Field(..., description="Код-во доступных страниц", examples=[3])
    items: List[ImageResponseItems]


class PremiereResponse(Base):
    total: int = Field(..., examples=[34])
    items: List[PremiereResponseItem]


class DigitalReleaseResponse(Base):
    page: int = Field(..., examples=[1])
    total: int = Field(..., examples=[34])
    releases: List[DigitalReleaseItem]


class VideoResponse(Base):
    total: int = Field(..., examples=[50])
    items: List[VideoResponseItems]


class KinopoiskUserVoteResponse(Base):
    total: int = Field(..., examples=[200])
    total_pages: int = Field(..., examples=[7])
    items: List[KinopoiskUserVoteResponseItems]


class ApiKeyResponse(Base):
    total_quota: ApiKeyResponseTotalQuota = Field(
        ...,
    )
    daily_quota: ApiKeyResponseDailyQuota = Field(
        ...,
    )
    account_type: AccountType = Field(..., examples=["FREE"])


class SeasonResponse(Base):
    total: int = Field(..., examples=[5])
    items: List[Season]


class DistributionResponse(Base):
    total: int = Field(..., examples=[5])
    items: List[Distribution]


class AwardResponse(Base):
    total: int = Field(..., examples=[5])
    items: List[Award]
