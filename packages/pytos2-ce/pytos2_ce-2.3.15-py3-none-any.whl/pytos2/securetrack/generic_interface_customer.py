from enum import Enum
from typing import Optional

from attr.converters import optional

from pytos2.models import Jsonable
from pytos2.utils import propify, prop

from netaddr import IPAddress


@propify
class GenericInterfaceCustomer(Jsonable):
    id: Optional[int] = prop(None, converter=optional(int))
    generic: Optional[bool] = prop(False)
    deviceId: Optional[int] = prop(None, converter=optional(int))
    interfaceName: str = prop(None)
    customerId: Optional[int] = prop(None, converter=optional(int))
