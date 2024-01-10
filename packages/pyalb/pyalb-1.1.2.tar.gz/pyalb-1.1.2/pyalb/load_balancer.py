from __future__ import annotations

from uuid import uuid4
import typing as t
from abc import ABC, abstractmethod

import requests
from flask import Flask, Response, make_response

from .health_checker import IHealthChecker, HealthChecker
from .server import IServer, Server
from .routing import SUPPORTED_ROUTING_ALGORITHMS, RoutingContext


class IHttpServer(ABC):
    _app: t.Any = None

    @abstractmethod
    def run(self):
        """Implement this to run http server"""

    @abstractmethod
    def _home(self, backend_server: str) -> t.Any:
        """Implement this to serve request on given backend server"""


class HttpServer(IHttpServer):
    _app: Flask = None

    def __init__(self, host: str = "127.0.0.1", port: int = 5000):
        self._host = host
        self._port = port
        self._app = Flask(__name__)
        self._app.add_url_rule("/", view_func=self._home)

    def run(self):
        self._app.run(host=self._host, port=self._port)

    def _home(self, backend_server: IServer) -> t.Any:
        backend_server_address = backend_server.url
        response_content, status_code = self._serve_request(backend_server_address)
        return response_content, status_code

    def _serve_request(self, backend_server_address: str) -> t.Tuple[t.Any, int]:
        response: Response = requests.get(backend_server_address, timeout=1)
        return response.content, response.status_code


class LoadBalancer(HttpServer):
    _servers: t.List[IServer] = None
    _health_checker: IHealthChecker = None

    def __init__(
        self,
        host: str,
        port: int,
        healthcheck_endpoint: str,
    ):
        self._health_checker = HealthChecker(healthcheck_endpoint)
        super().__init__(host, port)

    def register_servers(self, servers: t.List[IServer]) -> None:
        self._servers = [Server(server_id=uuid4(), url=server) for server in servers]
        print(f"servers registered: {self._servers}")

    def register_routing(self, routing_algorithm: str) -> None:
        self.routing_ctx = RoutingContext(
            routing_strategy=SUPPORTED_ROUTING_ALGORITHMS[routing_algorithm](
                self._servers
            )
        )
        print(f"registered routing algorithm: {self.routing_ctx.routing_strategy}")

    def _home(self) -> t.Any:
        backend_server: IServer = self.routing_ctx.route()
        response_content, status_code = super()._home(backend_server)
        return make_response(response_content, status_code)

    def run(self):
        self._health_checker.start(servers=self._servers)
        super().run()


def init_alb(host: str, port: int, healthcheck_endpoint: str) -> LoadBalancer:
    return LoadBalancer(host=host, port=port, healthcheck_endpoint=healthcheck_endpoint)
