from json import JSONDecodeError

from typing import Union, Optional, Iterator, List
from enum import Enum

from traversify import Traverser
from pathlib import Path

# avoid circular imports
import pytos2
from .api import ScwAPI
from requests import Response
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

from pytos2.securechange.user import classify_user_object, SCWParty, SCWUser
from pytos2.securechange.device import DeviceExclusions

from pytos2.utils import NoInstance, get_api_node
from pytos2.utils.cache import Cache, CacheIndex


class Scw:
    default: Union["Scw", NoInstance] = NoInstance(
        "Scw.default",
        "No Scw instance has been initialized yet, initialize with `Scw(*args, **kwargs)`",
    )

    def __init__(
        self,
        hostname: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        default=True,
    ):
        self.api: ScwAPI = ScwAPI(hostname, username, password)
        if default:
            Scw.default = self

        self.user_cache = Cache()
        self.users_by_name = self.user_cache.make_index("name")
        self.users_by_id = self.user_cache.make_index("id")

    def ticket_search(
        self,
        subject: Optional[str] = None,
        requester: Optional[str] = None,
        group: Optional[str] = None,
        assigned_to: Optional[str] = None,
        priority: Optional[str] = None,
        status: Optional[Union[str, "pytos2.securechange.ticket.Task.Status"]] = None,
        sla_status: Optional[
            Union[str, "pytos2.securechange.ticket.Ticket.SlaStatus"]
        ] = None,
        field_name: Optional[str] = None,
        field_value: Optional[str] = None,
        current_step: Optional[str] = None,
        expiration_date_from: Optional[str] = None,
        expiration_date_to: Optional[str] = None,
        domain_name: Optional[str] = None,
    ) -> List["pytos2.securechange.ticket.TicketSearchResult"]:
        # params are everything but self

        params = {key: value for (key, value) in locals().items() if key != "self"}

        from pytos2.securechange.ticket import (
            TicketSearchResult,
            TicketStatus,
            Ticket,
            Task,
        )

        for k, param in params.items():
            if isinstance(param, Enum):
                params[k] = param.value

        r = self.api.session.get("tickets/search", params=params)
        if not r.ok:
            r.raise_for_status()
        else:
            tickets = get_api_node(
                r.json(), "tickets_search_results.ticket_result", listify=True
            )
            return [TicketSearchResult.kwargify(t) for t in tickets]

    def get_users(
        self,
        show_indirect_relation: Optional[bool] = None,
        user_name: Optional[str] = None,
        email: Optional[str] = None,
        exact_name: Optional[bool] = None,
    ) -> List[SCWParty]:
        params = {}
        if show_indirect_relation:
            params["showIndirectRelation"] = show_indirect_relation
        if user_name:
            params["user_name"] = user_name
        if email:
            params["email"] = email
        if exact_name:
            params["exact_name"] = exact_name

        response = self.api.session.get("users", params=params)
        if not response.ok:
            response.raise_for_status()
        else:
            _json = response.json()
            users_node = get_api_node(_json, "users.user", listify=True)

            users = []
            self.user_cache.clear()

            for obj in users_node:
                user = classify_user_object(obj)
                users.append(user)

            self.user_cache.set_data(users)
            return users

    def _get_user_from_server(self, identifier: int) -> SCWParty:
        response = self.api.session.get(f"users/{identifier}")

        # if not response.ok:
        response.raise_for_status()
        # else:
        _json = response.json()

        key = ""
        if "group" in _json:
            key = "group"
        elif "user" in _json:
            key = "user"
        else:
            raise KeyError(
                f"Root user class key {_json.keys()} not currently supported by pytos2"
            )

        user_json = _json[key]
        if isinstance(user_json, list):
            user_json = user_json[0]
        return classify_user_object(user_json, obj_type=key)

    def get_user(
        self,
        identifier: Union[str, int],
        expand: bool = False,
        update_cache: Optional[bool] = None,
    ) -> SCWParty:
        if update_cache is not False and self.user_cache.is_empty():
            _ = self.get_users()  # create or update cache

        if isinstance(identifier, str):
            user = self.users_by_name.get(identifier)
            if not user:
                _ = self.get_users()
                user = self.users_by_name.get(identifier)
                if not user:
                    raise ValueError(f"User with name {identifier} not found")

            if expand:
                # this API only give @xsi.type as additional info
                return self._get_user_from_server(user.id)
            else:
                return user
        else:
            user = self.users_by_id.get(identifier)
            if not user:
                _ = self.get_users()
                user = self.users_by_id.get(identifier)
            if not user:
                raise ValueError(f"User with id {identifier} not found")

            if expand:
                try:
                    return self._get_user_from_server(identifier)
                except HTTPError as e:
                    # wrap the HTTPError into ValueError for consisency
                    raise ValueError(f"User with id {identifier} not found got {e}")
            else:
                return user

    def get_excluded_device_ids(self, show_all: Optional[bool] = None) -> List[int]:
        url = f"devices/excluded"
        if isinstance(show_all, bool):
            url += "?show_all="
            show_all = str(show_all).lower()
            url += show_all

        r = self.api.session.get(url)
        if r.ok:
            excludes_json = r.json()
            device_ids_model = DeviceExclusions.kwargify(excludes_json)
            return device_ids_model.device_ids
        else:
            r.raise_for_status()

    def get_tickets(
        self,
        status: Optional[
            Union[
                "pytos2.securechange.ticket.TicketStatus",
                List["pytos2.securechange.ticket.TicketStatus"],
            ]
        ] = None,
        start: Optional[int] = None,
        descending: Optional[bool] = None,
        expand_links: Optional[bool] = None,
    ) -> List["pytos2.securechange.ticket.TicketIterator"]:
        from pytos2.securechange.ticket import TicketStatus, TicketIterator

        params = {}

        if status is not None:
            if isinstance(status, list):
                params["status"] = ",".join([s.value for s in status])
            else:
                params["status"] = status.value
        if start is not None:
            params["start"] = start
        if descending is not None:
            params["desc"] = "true" if descending else "false"
        if expand_links is not None:
            params["expand_links"] = "true" if expand_links else "false"

        return list(TicketIterator(self.api.session, params))

    def get_ticket(self, _id: int) -> "pytos2.securechange.ticket.Ticket":
        from pytos2.securechange.ticket import Ticket

        r = self.api.session.get(f"tickets/{_id}")
        if r.ok:
            tkt = Ticket.kwargify(r.json())
            return tkt
        else:
            r.raise_for_status()

    def reassign_ticket(
        self,
        ticket,
        user,
        step: Union[None, "Step", int, str] = None,
        task: Union[None, "Task", int] = None,
        comment="",
    ) -> None:
        from pytos2.securechange.ticket import Step, Task, Ticket

        if not isinstance(ticket, Ticket):
            ticket = self.get_ticket(ticket)

        if not isinstance(user, SCWUser):
            user = Scw.default.get_user(user)

        if step is None:
            step = ticket.current_step

        if not isinstance(step, Step):
            step = ticket.get_step(step)

        if task is None:
            task = step.get_task(0)

        if not isinstance(task, Task):
            task = step.get_task(task)

        try:
            response = self.api.session.put(
                f"tickets/{ticket.id}/steps/{step.id}/tasks/{task.id}/reassign/{user.id}",
                json={"reassign_task_comment": {"comment": comment}},
            )
            if not response.ok:
                msg = response.json().get("result").get("message")
                response.raise_for_status()
        except HTTPError as e:
            raise ValueError(
                f"Got {e}, with Error Message: {msg}. Only tasks under current step can be reassigned"
            )

    def get_attachment(self, file_id: Union[int, str]) -> bytes:
        response = self.api.session.get(f"attachments/{file_id}")
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Getting Attachment: {e}")
        return response.content

    def add_attachment(self, file: str) -> str:
        attachment = {"attachment": open(file, "rb")}
        response = self.api.session.post("attachments", files=attachment)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Adding Attachment: {e}")
        return response.text

    def add_comment(
        self,
        ticket_id: Union[int, str],
        step_id: Union[int, str],
        task_id: Union[int, str],
        comment_content: str,
        attachment_uuids: Optional[List[str]],
    ) -> str:
        def _format_attachments(uuids: List[str]) -> dict:
            return {"attachment": [{"uid": id} for id in uuids]}

        comment = {"comment": {"content": comment_content}}
        if attachment_uuids:
            comment["comment"]["attachments"] = _format_attachments(attachment_uuids)

        response = self.api.session.post(
            f"tickets/{ticket_id}/steps/{step_id}/tasks/{task_id}/comments",
            json=comment,
        )
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Adding Comment: {e}")

        return response.text

    def delete_comment(
        self,
        ticket_id: Union[int, str],
        comment_id: Union[int, str],
    ) -> None:
        response = self.api.session.delete(
            f"tickets/{ticket_id}/comments/{comment_id}",
        )
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Deleting Comment: {e}")

    def get_ticket_history(self, _id: int):
        from pytos2.securechange.ticket import TicketHistory

        try:
            response = self.api.session.get(f"tickets/{_id}/history")
            response.raise_for_status()
            response_json = response.json()
            ticket_history = TicketHistory.kwargify(
                response_json["ticket_history_activities"]
            )
            return ticket_history
        except JSONDecodeError:
            raise ValueError(f"Error decoding json: {response.text}")
        except ValueError as e:
            raise ValueError(f"Error creating ticket_history class: {e}")
        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            raise ValueError(f"Error retrieving ticket_history: {e}")
