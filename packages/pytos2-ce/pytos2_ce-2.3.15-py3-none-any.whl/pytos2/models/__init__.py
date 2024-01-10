from typing import Optional, Union

from enum import Enum

import attr

from pytos2.utils import jsonify, kwargify, propify, prop


@propify
class Jsonable:
    class Prop(Enum):
        XSI_TYPE = "@xsi.type"

    data: Optional[dict] = attr.ib(None, eq=False, repr=False)
    id: Optional[int] = attr.ib(None, eq=False)
    xsi_type: Optional[Union[str, Enum]] = prop(
        None, key=Prop.XSI_TYPE.value, repr=False
    )
    _flatifies: dict = attr.ib(factory=dict, repr=False)

    _json_override: Optional[dict] = attr.ib(None, eq=False, repr=False, init=False)

    @property
    def _json(self) -> dict:
        return self._json_override or jsonify(self)

    @_json.setter
    def _json(self, val):
        self._json_override = val

    @classmethod
    def kwargify(cls, obj: dict):
        _obj, kwargs = kwargify(cls, obj)
        return cls(**kwargs)  # type: ignore

    def __getitem__(self, key):
        return getattr(self, key)


class UnMapped(dict):
    def __init__(self, obj: dict):
        super().__init__(obj)
        self._json = obj
        self.data = obj
        self._type = "UnMapped"

    @classmethod
    def kwargify(cls, obj: dict):
        return cls(obj)
