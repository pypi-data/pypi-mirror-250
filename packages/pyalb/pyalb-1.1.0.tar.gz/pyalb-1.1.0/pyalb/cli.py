import argparse
import logging
import typing as t

from pyalb import __version__
from .routing.strategies import __all__

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def init_cli() -> t.Any:
    parser = argparse.ArgumentParser(
        prog="pyalb",
        description="An application load balancer",
        epilog="Thanks for using pyalb!",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        default=argparse.SUPPRESS,
        version="%(prog)s (version " + __version__ + ")\n",
        help="show program's version number and exit",
    )
    parser.add_argument(
        "--servers",
        "-S",
        nargs="+",
        required=True,
        action="extend",
        dest="servers",
        help="list of backend server urls",
    )
    parser.add_argument(
        "--routing",
        "-R",
        type=str,
        default="RoundRobbin",
        dest="routing",
        choices=__all__,
        help="Routing algorithm to use [default: RoundRobbin]",
    )
    parser.add_argument(
        "--host",
        "-H",
        type=str,
        default="127.0.0.1",
        dest="host",
        help="host to use by pyalb [default: 127.0.0.1]",
    )
    parser.add_argument(
        "--port",
        "-P",
        type=str,
        default="5000",
        dest="port",
        help="port to use by pyalb [default: 5000]",
    )
    parser.add_argument(
        "--healthcheck-endpoint",
        "-HCE",
        type=str,
        default="/health",
        dest="healthcheck_endpoint",
        help="health check endpoint for your backend servers. "
        + "pyalb will call this endpoint to check health of your backend servers "
        + "[default: /health]",
    )
    args = parser.parse_args()
    return args
