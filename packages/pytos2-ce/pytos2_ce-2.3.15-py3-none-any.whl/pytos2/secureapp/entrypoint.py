from typing import Union, Optional, List

from result import Result
from requests import Response
from requests.exceptions import HTTPError

# avoid circular imports
import pytos2  # noqa
from .api import SaAPI
from pytos2.utils import NoInstance, get_api_node
from .application_identities import ApplicationIdentity


class Sa:
    default: Union["Sa", NoInstance] = NoInstance(
        "Sa.default",
        "No Sa instance has been initialized yet, initialize with `Sa(*args, **kwargs)`",
    )

    def __init__(
        self,
        hostname: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        default=True,
    ):
        self.api: SaAPI = SaAPI(hostname, username, password)
        if default:
            Sa.default = self

        self._application_identities: List[ApplicationIdentity] = []

    @property
    def application_identities(self) -> List[ApplicationIdentity]:
        if not self._application_identities:
            res = self._get_application_identities()
            self._application_identities = res
        return self._application_identities

    def _get_application_identities(
        self, cache=True
    ) -> Result[List[ApplicationIdentity], Response]:
        res = self.api.get_application_identities()
        if res.ok:
            return [
                ApplicationIdentity.kwargify(a)
                for a in get_api_node(
                    res.json(),
                    "application_identities.application_identity",
                    listify=True,
                )
            ]
        else:
            try:
                msg = res.text
                res.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"got '{msg}' from API Error :{e}")
