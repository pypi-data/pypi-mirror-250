import sys
import inspect

from .base import IRoutingStrategy
from .context import RoutingContext
from .strategies import *

SUPPORTED_ROUTING_ALGORITHMS = {
    cls.__name__: cls
    for _, cls in inspect.getmembers(sys.modules[__name__], inspect.isclass)
    if issubclass(cls, IRoutingStrategy)
}


__all__ = ["SUPPORTED_ROUTING_ALGORITHMS", "RoutingContext"]
