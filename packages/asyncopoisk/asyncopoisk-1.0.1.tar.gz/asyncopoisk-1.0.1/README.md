# [Asyncopoisk](https://github.com/Ninnjah/asyncopoisk)
Это асинхронная обертка для [Kinopoisk API Unofficial](https://kinopoiskapiunofficial.tech/). Создавалась для личного пользования, так как удобной и асинхронной обертки найти не смог. Это был мой первый опыт в написании АПИ обертки, так что PR и Issue приветствуются!

# Особенности
В обертки реализованы все методы, что были описаны в [документации](https://kinopoiskapiunofficial.tech/documentation/api/) на момент *2023.21.12* структура запросов сделана так, чтобы минимально отличаться от [документации](https://kinopoiskapiunofficial.tech/documentation/api/) самой АПИ

# Начало работы
Перед использованием asyncopoisk вам нужно получить токен. Получить его можно на сайте [Kinopoisk API Unofficial](https://kinopoiskapiunofficial.tech/)

Установите Asyncopoisk
```shell
pip install asyncopoisk
```

Далее создайте экземпляр обертки
```python
from asyncopoisk import KinopoiskAPI
kp = KinopoiskAPI(token="TOKEN")
```
Теперь с помощью `kp` вы можете вызывать методы АПИ.

> *ВАЖНО* так как обертка использует асинхронную httpx сессию, вызов всех методов должен происходить асинхронно

# Примеры
**Получить данные о фильме по kinopoisk id**
```python
import asyncio
from asyncopoisk import KinopoiskAPI


async def main(kp_token: str, kp_id: int):
    kp = KinopoiskAPI(token=kp_token)
    # Получаем фильм по id
    film = await kp.films(kp_id)


if __name__ == "__main__":
    asyncio.run(main(kp_token="TOKEN", kp_id=841700))
```

**Получить данные о фильме по imdb id**
```python
import asyncio
from asyncopoisk import KinopoiskAPI


async def main(kp_token: str, imdb_id: str):
    kp = KinopoiskAPI(token=kp_token)
    # Получаем фильм по imdb id
    film = await kp.films(imdb_id=imdb_id)


if __name__ == "__main__":
    asyncio.run(main(kp_token="TOKEN", imdb_id="tt3659388"))
```

**Получить список русских сериалов с рейтингом не ниже 6.5 от 2023 года**
> Номера стран и жанров можно получить используя метод `films.filters()`
```python
from typing import List

import asyncio
from asyncopoisk import KinopoiskAPI
from asyncopoisk.models.enums import SearchOrder, SearchFilmType


async def main(
	kp_token: str, 
    countries: List[int],
    order: SearchOrder,
    type: SearchFilmType,
    rating_from: float,
    year_from: int,
):
    kp = KinopoiskAPI(token=kp_token)
    # Поиск по фильтрам
    film = await kp.films(
        countries=countries,
        order=order,
        type=type,
        rating_from=rating_from,
        year_from=year_from,
    )


if __name__ == "__main__":
    asyncio.run(
        main(
            kp_token="TOKEN", 
            countries = [34],
            order = SearchOrder.RATING,
            type = SearchFilmType.TV_SERIES,
            rating_from = 6.5,
            year_from = 2023,
        )
    )
```

**Поиск по ключевому слову**
```python
import asyncio
from asyncopoisk import KinopoiskAPI
from asyncopoisk.models.enums import SearchOrder, SearchFilmType


async def main(kp_token: str, keyword: str):
    kp = KinopoiskAPI(token=kp_token)
    # Поиск по ключевому слову
    result = await kp.films.search_by_keyword(keyword=keyword)


if __name__ == "__main__":
    asyncio.run(
        main(
            kp_token="2d3c7c68-b288-4fbd-84d8-ccb68e495923",
            keyword="Марсианин",
        )
    )
```

# Зависимости
- [pydantic 2.3.0](https://github.com/pydantic/pydantic)
- [httpx 0.25.0](https://github.com/encode/httpx)