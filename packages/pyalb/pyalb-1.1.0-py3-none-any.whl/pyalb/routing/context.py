from .base import IRoutingStrategy
from ..server import IServer


class RoutingContext:
    def __init__(self, routing_strategy: IRoutingStrategy) -> None:
        self._routing_strategy = routing_strategy

    @property
    def routing_strategy(self):
        return self._routing_strategy

    def route(self) -> IServer:
        return self._routing_strategy.route()
