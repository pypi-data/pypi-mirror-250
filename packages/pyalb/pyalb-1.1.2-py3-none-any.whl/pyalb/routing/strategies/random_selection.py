import random
import typing as t

from ..base import IRoutingStrategy
from ...server import IServer


class RandomSelection(IRoutingStrategy):
    def __init__(self, servers: t.List[IServer]) -> None:
        self._servers = servers
        self._no_of_servers = len(self._servers)

    def route(self) -> IServer:
        server = self._get_next_random_server()
        return server

    def _get_next_random_server(self):
        random_chosen_server = self._servers[random.randint(0, self._no_of_servers - 1)]
        return random_chosen_server
