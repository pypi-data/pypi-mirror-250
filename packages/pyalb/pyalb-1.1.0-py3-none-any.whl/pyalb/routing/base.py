from abc import ABC, abstractmethod

from ..server import IServer


class IRoutingStrategy(ABC):
    @abstractmethod
    def route(self) -> IServer:
        pass
