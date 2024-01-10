from enum import Enum
from typing import Optional

from attr.converters import optional

from pytos2.models import Jsonable
from pytos2.utils import propify, prop

from netaddr import IPAddress


@propify
class GenericInterface(Jsonable):
    class Type(Enum):
        EXTERNAL = "external"
        INTERNAL = "internal"

    id: Optional[int] = prop(None, converter=optional(int))
    mgmtId: Optional[int] = prop(None, converter=optional(int))
    name: str = prop(None)
    ip: Optional[IPAddress] = prop(None)
    mask: Optional[IPAddress] = prop(None, repr=False)
    vrf: Optional[str] = prop(None)
    mpls: Optional[bool] = prop(False)
    unnumbered: Optional[bool] = prop(False)
    type: Optional[Type] = prop(None)
