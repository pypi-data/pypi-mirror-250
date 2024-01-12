from enum import Enum
from typing import List, Optional

from attr.converters import optional

from pytos2.models import Jsonable
from pytos2.utils import propify, prop


@propify
class GenericTransparentFirewall(Jsonable):
    id: Optional[int] = prop(None, converter=optional(int))
    outputL3DeviceId: Optional[int] = prop(None, converter=optional(int))
    outputL3IsGenericDevice: Optional[bool] = prop(None)
    outputL3InterfaceName: Optional[str] = prop(None)
    layer2DeviceId: Optional[int] = prop(None, converter=optional(int))
    inputL2InterfaceName: Optional[str] = prop(None)
    outputL2InterfaceName: Optional[str] = prop(None)
    inputL3DeviceId: Optional[int] = prop(None, converter=optional(int))
    inputL3IsGenericDevice: Optional[bool] = prop(None)
    inputL3InterfaceName: Optional[str] = prop(None)
