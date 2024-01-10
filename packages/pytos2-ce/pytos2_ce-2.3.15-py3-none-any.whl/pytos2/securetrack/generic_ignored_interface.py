from enum import Enum
from typing import Optional

from attr.converters import optional

from pytos2.models import Jsonable
from pytos2.utils import propify, prop

from netaddr import IPAddress


@propify
class GenericIgnoredInterface(Jsonable):
    id: Optional[int] = prop(None, converter=optional(int))
    interfaceName: str = prop(None)
    mgmtId: Optional[int] = prop(None, converter=optional(int))
    ip: Optional[IPAddress] = prop(None)
