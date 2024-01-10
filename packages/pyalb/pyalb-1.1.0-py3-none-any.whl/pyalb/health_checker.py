import os
import time
import typing as t
from threading import Thread
from abc import ABC, abstractmethod

import requests
from .server import IServer


class IHealthChecker(ABC):
    @abstractmethod
    def start(self, servers: t.List[IServer]) -> None:
        """Implement this method to start your health checker service,
        which will health check on given list of servers"""


class HealthChecker(IHealthChecker):
    _health_check_daemon: Thread = None
    _unhealthy_servers: t.Set[IServer] = set()

    def __init__(self, healthcheck_endpoint: str) -> None:
        self._health_check_endpoint = healthcheck_endpoint

    def start(self, servers: t.List[IServer]) -> None:
        self._health_check_daemon = Thread(
            target=self._health_check,
            name="health check daemon",
            kwargs={"servers": servers},
            daemon=True,
        )
        self._health_check_daemon.start()

    def _health_check(self, servers: t.List[IServer]) -> None:
        time.sleep(5)  # To let main process start
        while len(servers) != len(self._unhealthy_servers):
            for server in servers:
                try:
                    response = requests.get(
                        server.url + self._health_check_endpoint, timeout=1
                    )
                    response.raise_for_status()
                except (
                    requests.exceptions.ConnectionError,
                    requests.exceptions.HTTPError,
                ):
                    print(f"{server.url} server is unhealthy")
                    server.is_healthy = False
                if not server.is_healthy:
                    self._unhealthy_servers.add(server)
                else:
                    server.is_healthy = True
                    if server in self._unhealthy_servers:
                        self._unhealthy_servers.remove(server)
            time.sleep(10)  # Wait between consecutive healthchecks
        self._terminate_pyalb()

    @staticmethod
    def _terminate_pyalb():
        print("No healthy server found. Shutting down pyalb!!")
        os._exit(0)
