import typing as t

from ..base import IRoutingStrategy
from ...server import IServer


class RoundRobbin(IRoutingStrategy):
    def __init__(self, servers: t.List[IServer]) -> None:
        self._servers = servers
        self._max_servers = len(servers)
        self.server_idx = 0

    def cycle(self) -> IServer:
        if self.server_idx == self._max_servers:
            self.server_idx = 0
        chosen_server = self._servers[self.server_idx % self._max_servers]
        self.server_idx += 1
        return chosen_server

    def route(self) -> IServer:
        server = self._get_next_server()
        print(f"request routed using {self.__class__.__name__} on {server}")
        return server

    def _get_next_server(self) -> IServer:
        return self.cycle()
