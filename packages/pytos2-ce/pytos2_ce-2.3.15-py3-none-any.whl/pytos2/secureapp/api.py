from enum import Enum
from typing import Optional

from pytos2.api import get_app_api_session
from pytos2.utils import setup_logger


LOGGER = setup_logger("sa_api")


class SaAPI:
    class Meta(Enum):
        PATH = "securechangeworkflow/api/secureapp"
        APP = "SCW"
        TOS2_ENV = "SC_SERVER_SERVICE"

    def __init__(
        self, hostname: Optional[str], username: Optional[str], password: Optional[str]
    ):
        self.hostname, self.username, self.password, self.session = get_app_api_session(
            app=self, hostname=hostname, username=username, password=password
        )

    def get_application_identities(self):
        r = self.session.get("repository/application_identities")
        return r
