from httpx import Response


class KinopoiskException(Exception):
    def __init__(self, message: str = ""):
        super().__init__(message)


class BadRequest(KinopoiskException):
    def __init__(self, response: Response):
        self.message = f"{type(self).__name__}('{self}') - {response.content}"
        super().__init__(self.message)
