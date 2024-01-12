from os import getenv
from urllib.parse import urljoin, urlparse
import logging

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from traversify import Traverser  # type: ignore


from pytos2.utils import setup_logger

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
LOGGER = setup_logger("api")
REQUESTS_LOGGER = logging.getLogger("requests.packages.urllib3")


class APISession(requests.Session):

    """
    Inits a prefixed API session

    :param str base_url: The url for the tos host
    :param str username: username
    :param str password: password
    :param str api_path: api path to prefix all requests
    :param bool verify: sets ssl strict verification for all requests
    """

    def __init__(
        self,
        hostname,
        scheme="https",
        username=None,
        password=None,
        api_path="",
        verify=False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if username is not None and password is not None:
            self.auth = (username, password)

        if kwargs.get("headers") is None:
            self.headers.update({"Accept": "application/json, */*"})

        self.verify = verify
        host_base = urlparse(hostname)

        self.base_url = urljoin(
            f"{scheme}://" + (host_base.netloc or host_base.path),
            api_path.strip("/") + "/",
        )

    def request(self, method, url, *args, **kwargs):
        """Overrides all requests to prefix url, not intended to be used directly"""

        # Make sure we have a sensible timeout set
        if not kwargs.get("timeout", None):
            kwargs["timeout"] = 300
        REQUESTS_LOGGER.debug(f"Request kwargs {kwargs}")

        response = super().request(method, urljoin(self.base_url, url), *args, **kwargs)
        REQUESTS_LOGGER.debug(f"Response body {response.text}")
        return response


def get_app_api_session(app, hostname=None, username=None, password=None):
    app_identifier = app.Meta.APP.value.upper()
    app_path = app.Meta.PATH.value
    username_key = "{}_API_USERNAME".format(app_identifier)
    password_key = "{}_API_PASSWORD".format(app_identifier)
    hostname_key = "{}_HOSTNAME".format(app_identifier)

    tos2_env_host_key = "{}_HOST".format(app.Meta.TOS2_ENV.value)
    tos2_env_port_key = "{}_PORT".format(app.Meta.TOS2_ENV.value)

    tos2_host = getenv(tos2_env_host_key, None)
    tos2_port = getenv(tos2_env_port_key, None)

    is_tos2 = getenv(tos2_env_host_key, False)
    scheme = "https"

    hostname = hostname or tos2_host or getenv(hostname_key) or getenv("TOS_HOSTNAME")
    if not hostname:
        raise ValueError(
            f"hostname argument must be provided if {hostname_key} or TOS_HOSTNAME environment variable is not set"
        )
    username = username or getenv(username_key)
    if not username:
        raise ValueError(
            f"username argument must be provided if {username_key} environment variable is not set"
        )
    password = password or getenv(password_key)
    if not password:
        raise ValueError(
            f"password argument must be provided if {password_key} environment variable is not set"
        )

    if is_tos2:
        try:
            tos2_port = int(tos2_port)
        except ValueError:
            tos2_port = 443
        scheme = "https" if tos2_port == 443 else "http"

    return (
        hostname,
        username,
        password,
        APISession(
            hostname=hostname,
            scheme=scheme,
            username=username,
            password=password,
            api_path=app_path,
        ),
    )


def resultify_response(response):
    if response.ok:
        return response
    else:
        response.raise_for_status()


def traversify_response(response):
    if response.ok:
        return Traverser(response)
    else:
        response.raise_for_status()


def boolify(params: dict) -> dict:
    return {k: str(v).lower() if isinstance(v, bool) else v for k, v in params.items()}
