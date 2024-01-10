from enum import Enum
from typing import Optional

from attr.converters import optional

from pytos2.models import Jsonable
from pytos2.utils import propify, prop

from netaddr import IPAddress


@propify
class GenericRoute(Jsonable):
    id: Optional[int] = prop(None, converter=optional(int))
    mgmtId: Optional[int] = prop(None, converter=optional(int))
    destination: Optional[IPAddress] = prop(None)
    mask: Optional[IPAddress] = prop(None, repr=False)
    interfaceName: str = prop(None)
    nextHop: Optional[str] = prop(None)
    nextHopType: Optional[str] = prop(None)
    vrf: Optional[str] = prop(None)
