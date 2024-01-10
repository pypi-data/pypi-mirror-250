class IServer:
    id: str
    url: str
    is_healthy: bool


class Server(IServer):
    def __init__(self, server_id: str, url: str, is_healthy: bool = True) -> None:
        self._id = server_id
        self._url = url
        self._is_healthy = is_healthy

    @property
    def id(self) -> str:
        return self._id

    @property
    def url(self) -> str:
        return self._url

    @property
    def is_healthy(self) -> bool:
        return self._is_healthy

    @is_healthy.setter
    def is_healthy(self, value: bool) -> None:
        self._is_healthy = value
