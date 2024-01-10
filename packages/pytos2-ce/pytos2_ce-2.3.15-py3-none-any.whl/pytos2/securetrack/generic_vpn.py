from enum import Enum
from typing import Optional

from attr.converters import optional

from pytos2.models import Jsonable
from pytos2.utils import propify, prop

from netaddr import IPAddress


@propify
class GenericVpn(Jsonable):
    id: Optional[int] = prop(None, converter=optional(int))
    deviceId: Optional[int] = prop(None, converter=optional(int))
    generic: Optional[bool] = prop(None)
    interfaceName: Optional[str] = prop(None)
    tunnelSourceIpAddr: Optional[IPAddress] = prop(None, repr=False)
    tunnelDestIpAddr: Optional[IPAddress] = prop(None, repr=False)
