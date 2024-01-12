from collections import OrderedDict
from datetime import date
from typing import Dict, Iterable, Iterator, List, Tuple, Optional, Union
from io import BytesIO
import typing

from requests.exceptions import HTTPError
from requests import Response

from pytos2.securetrack.generic_transparent_firewall import GenericTransparentFirewall

from .api import StAPI
from .device import Device
from .domain import Domain
from .network_object import classify_network_object, NetworkObject
from .policy_browser import Emptiness
from .revision import Revision
from .rule import BindingPolicy, Documentation, SecurityRule
from pytos2.utils import (
    NoInstance,
    get_api_node,
    sanitize_uid,
    uids_match,
    setup_logger,
)
from pytos2.utils.cache import Cache
from .service_object import classify_service_object, Service
from .zone import Zone, ZoneReference, ZoneEntry
from .interface import Interface, BindableObject, TopologyInterface
from .generic_device import GenericDevice
from .generic_ignored_interface import GenericIgnoredInterface
from .generic_interface_customer import GenericInterfaceCustomer
from .generic_interface import GenericInterface
from .generic_route import GenericRoute
from .generic_vpn import GenericVpn
from .join_cloud import JoinCloud
from .topology import TopologySyncStatus

LOGGER = setup_logger("st_entrypoint")


def _bool(x: bool) -> str:
    return "true" if x else "false"


def _querify(k: str, v: Union[str, bool, List[Union[str, bool]]]) -> str:
    # Used in `St.search_rules`. See that method for more details.

    # `search_text` params (key:values pairs with semantic key meanings to
    # Policy Browser, such as `'action:accept'`) are specified in the URI in
    # the format: `'key:value+key:value+...'`.  (e.g.:
    # `uid:123+action:accept`), so we have to marshal the given params into
    # said format.
    #
    # `strs remains strings, `bool`s are converted to the string `"true"` or
    # `"false"` respectively, and array values are converted to look like:
    # `'key:value1+key:value2+...'`.
    if isinstance(v, list):
        return " ".join([_querify(k, v_) for v_ in v])
    elif isinstance(v, bool):
        return f"{k}:{_bool(v)}"
    else:
        return f"{k}:{v}"


class St:
    default: Union["St", NoInstance] = NoInstance(
        "St.default",
        "No St instance has been initialized yet, initialize with `St(*args, **kwargs)`",
    )

    def __init__(
        self,
        hostname: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        default=True,
        cache=True,
    ):
        self.api: StAPI = StAPI(hostname, username, password)
        if default:
            St.default = self
        self.cache = cache

        self._devices_cache = Cache()
        self._devices_index = self._devices_cache.make_index(["name", "id"])

        self._network_objects_by_device_id_by_name: dict = {}
        self._network_objects_by_uid: dict = {}
        self._services_by_uid: dict = {}
        self._services_by_device_id_by_name: dict = {}
        self._device_rules_dict: dict = {}
        self._revision_rules_dict: dict = {}
        self._revisions_dict: dict = {}
        self._device_revisions_dict: dict = {}
        self._rules_dict: dict = {}
        self._zones_cache = Cache()
        self._zones_index = self._zones_cache.make_index(["name", "id"])
        self._zones: list = []
        self._zones_dict: dict = {}
        self._domains_cache = Cache()
        self._domains_index = self._domains_cache.make_index(["name", "id"])
        self._domains: list = []
        self._domains_dict: dict = {}

        self._generic_devices_cache = Cache()
        self._generic_devices_index = self._generic_devices_cache.make_index(
            ["name", "id"]
        )

    def _prime_generic_devices_cache(self):
        generic_devices = self.get_generic_devices(cache=False)

        self._generic_devices_cache.clear()
        for d in generic_devices:
            self._generic_devices_cache.add(d)

    def _prime_domains_cache(self):
        domains = self.api.session.get("domains").json()

        self._domains_cache.clear()
        for domain in get_api_node(domains, "domain", listify=True):
            domain_obj = Domain.kwargify(domain)
            self._domains_cache.add(domain_obj)

    def _prime_zones_cache(self):
        zones = self.api.session.get("zones").json()

        self._zones_cache.clear()
        for zone in get_api_node(zones, "zones.zone", listify=True):
            zone_obj = Zone.kwargify(zone)
            self._zones_cache.add(zone_obj)

    def _prime_devices_cache(self):
        devices = self.api.session.get("devices").json()

        self._devices_cache.clear()
        for device in get_api_node(devices, "devices.device", listify=True):
            device_obj = Device.kwargify(device)
            self._devices_cache.add(device_obj)

    def get_devices(self, cache: Optional[bool] = None, filter: Optional[dict] = None):
        if cache is not False and self.cache:
            if self._devices_cache.is_empty():
                self._prime_devices_cache()

            if not filter:
                return self._devices_cache.get_data()
            else:
                return [
                    d
                    for d in self._devices_cache.get_data()
                    if set(filter.items()).issubset(set(d.data.items()))
                ]
        else:
            devices = self.api.session.get("devices").json()
            d_list = [
                Device.kwargify(d)
                for d in get_api_node(devices, "devices.device", listify=True)
            ]
            if not filter:
                return d_list
            else:
                return [
                    d
                    for d in d_list
                    if set(filter.items()).issubset(set(d.data.items()))
                ]

    def get_zones(self, cache: Optional[bool] = None):
        if cache is not False and self.cache:
            if self._zones_cache.is_empty():
                self._prime_zones_cache()
            return self._zones_cache.get_data()
        else:
            zones = self.api.session.get("zones").json()
            return [
                Zone.kwargify(d)
                for d in get_api_node(zones, "zones.zone", listify=True)
            ]

    def _resolve_zone_from_name(self, name: Union[str, List[str]]):
        zones = self.get_zones()
        if isinstance(name, str):
            name = [name]

        objects = []

        for n in name:
            for zone in zones:
                if zone.name == n:
                    objects.append(zone)

        return objects

    def get_zone_subnets(
        self, identifier: Union[int, str, List[int]]
    ) -> List[ZoneEntry]:
        def _send_request(id_list):
            _identifier = ",".join([str(i) for i in id_list])
            response = self.api.session.get(f"zones/{_identifier}/entries")
            if not response.ok:
                try:
                    msg = response.json().get("result").get("message")
                    response.raise_for_status()
                except HTTPError as e:
                    raise ValueError(
                        f"wrong zone identifier, got '{msg}' from API Error: {e}"
                    )
            else:
                zone_entries = get_api_node(
                    response.json(), "zone_entries.zone_entry", listify=True
                )
                zone_subnets = []
                for entry in zone_entries:
                    zone_subnets.append(ZoneEntry.kwargify(entry))

                return zone_subnets

        def _get(_identifier):
            if isinstance(_identifier, str):
                _identifier = [z.id for z in self._resolve_zone_from_name(_identifier)]

            if isinstance(_identifier, (list, int)):
                if isinstance(_identifier, int):
                    _identifier = [_identifier]

                if isinstance(_identifier, list):
                    i = 0
                    length = len(_identifier)
                    res_subnets = []
                    while i < length:
                        id_list = _identifier[i : i + 10]
                        i += 10

                        for entry in _send_request(id_list):
                            res_subnets.append(entry)
                            # yield entry

                    return res_subnets  # noqa
            else:
                raise TypeError(
                    f"input identifier can only be list, int, str or list[int]] but got {_identifier}"
                )

        zone_subnets = []
        for entry in _get(identifier):
            zone_subnets.append(entry)
        return zone_subnets

    def get_zone_descendants(
        self, identifier: Union[int, str, List[int]]
    ) -> List[ZoneReference]:
        def _send_request(id_list):
            _identifier = ",".join([str(i) for i in id_list])

            response = self.api.session.get(f"zones/{_identifier}/descendants")
            if not response.ok:
                try:
                    msg = response.json().get("result").get("message")
                    response.raise_for_status()
                except HTTPError as e:
                    raise ValueError(
                        f"wrong zone identifier, got '{msg}' from API Error: {e}"
                    )
            else:
                zones = get_api_node(response.json(), "zones.zone", listify=True)
                if not zones:
                    raise ValueError(f"can not find zones by given ids: {_identifier}")
                zone_ref = []
                for zone in zones:
                    zone_ref.append(ZoneReference.kwargify(zone))

                return zone_ref

        def _get(_identifier):
            if isinstance(_identifier, str):
                _identifier = [z.id for z in self._resolve_zone_from_name(_identifier)]

            if isinstance(_identifier, (list, int)):
                if isinstance(_identifier, int):
                    _identifier = [_identifier]

                if isinstance(_identifier, list):
                    i = 0
                    length = len(_identifier)
                    res_descendants = []
                    while i < length:
                        id_list = _identifier[i : i + 10]
                        i += 10

                        for zone in _send_request(id_list):
                            res_descendants.append(zone)

                    return res_descendants
            else:
                raise TypeError(
                    f"input identifier can only be list, int, str or list[int]] but got {_identifier}"
                )

        zone_descendants = []
        for zone in _get(identifier):
            zone_descendants.append(zone)
        return zone_descendants

    def get_zone(
        self, identifier: Union[int, str], cache: Optional[bool] = None
    ) -> Optional[Zone]:
        def _get(_identifier):
            if isinstance(_identifier, int):
                zone = get_api_node(self.api.get_zone_by_id(_identifier).json(), "zone")
                return Zone.kwargify(zone) if zone else None
            else:
                for zone in get_api_node(
                    self.api.get_zones_by_name(_identifier).json(),
                    "zones.zone",
                    default=[],
                ):
                    zone_obj = Zone.kwargify(zone)
                    if zone_obj.name == _identifier:
                        return zone_obj

        if cache is not False and self.cache:
            if self._zones_cache.is_empty():
                self._prime_zones_cache()
            return self._zones_index.get(identifier)
        else:
            return _get(identifier)

    def get_domains(self, cache: Optional[bool] = None):
        if cache is not False and self.cache:
            if self._domains_cache.is_empty():
                self._prime_domains_cache()
            return self._domains_cache.get_data()
        else:
            domains = self.api.session.get("domains").json()

            return [
                Domain.kwargify(d)
                for d in get_api_node(domains, "domain", listify=True)
            ]

    def get_domain(
        self, identifier: Union[int, str], cache: Optional[bool] = None
    ) -> Optional[Domain]:
        def _get(_identifier):
            if isinstance(_identifier, int):
                domain = get_api_node(
                    self.api.get_domain_by_id(_identifier).json(), "domain"
                )
                return Domain.kwargify(domain) if domain else None
            else:
                for domain in get_api_node(
                    self.api.get_domains_by_name(_identifier).json(),
                    "domain",
                    default=[],
                ):
                    domain_obj = Domain.kwargify(domain)
                    if domain_obj.name == _identifier:
                        return domain_obj

        if cache is not False and self.cache:
            if self._domains_cache.is_empty():
                self._prime_domains_cache()
            return self._domains_index.get(identifier)
        else:
            return _get(identifier)

    def add_domain(
        self,
        name: str,
        description: Optional[str] = None,
        address: Optional[str] = None,
    ) -> Optional[Domain]:
        res = self.api.post_domain(name=name, description=description, address=address)
        if res.ok:
            created_url = res.headers.get("Location", "")
            did = int(created_url.split("/")[-1])
            new_domain = get_api_node(self.api.get_domain_by_id(did).json(), "domain")
            if new_domain:
                return Domain.kwargify(new_domain)
            else:
                raise ValueError(
                    f"domain id: {did} not found by GET call after POSTing to SecureTrack"
                )

        else:  # pragma: no cover
            try:
                msg = res.json().get("result").get("message")
                res.raise_for_status()
            except HTTPError as e:
                raise ValueError(
                    f"unable to POST new domain :{name} to SecureTrack, got {msg} from API Error: {e}"
                )

    def update_domain(
        self,
        identifier: Union[int, str],
        name: Optional[str] = None,
        description: Optional[str] = None,
        address: Optional[str] = None,
    ) -> Optional[Domain]:
        if self._domains_cache.is_empty():
            self._prime_domains_cache()
        modify_domain = self._domains_index.get(identifier)
        res = self.api.put_domain(
            id=modify_domain.id,
            name=name or modify_domain.name,
            description=description or modify_domain.description,
            address=address or modify_domain.address,
        )
        if res.ok:
            modified_domain_json = get_api_node(
                self.api.get_domain_by_id(modify_domain.id).json(), "domain"
            )
            modified_domain = Domain.kwargify(modified_domain_json)
            self._domains_dict[identifier] = modified_domain
            return modified_domain

        else:
            try:
                msg = res.json().get("result").get("message")
                res.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Got {e}, with Error Message: {msg}")

    def get_device(
        self, identifier: Union[int, str], cache: Optional[bool] = None
    ) -> Optional[Device]:
        def _get(_identifier):
            if isinstance(_identifier, int):
                device = get_api_node(
                    self.api.get_device_by_id(identifier).json(), "device"
                )
                return Device.kwargify(device) if device else None
            else:
                for device in get_api_node(
                    self.api.get_devices_by_name(_identifier).json(),
                    "devices.device",
                    default=[],
                ):
                    device_obj = Device.kwargify(device)
                    if device_obj.name == _identifier:
                        return device_obj

        if cache is not False and self.cache:
            if self._devices_cache.is_empty():
                self._prime_devices_cache()
            return self._devices_index.get(identifier)
        else:
            return _get(identifier)

    def _prime_network_objects_cache(self, device_id: int):
        # bust existing cache for device_id
        self._network_objects_by_device_id_by_name[device_id] = {}
        self._network_objects_by_uid = {
            u: [o for o in objs if o.device_id != device_id]
            for u, objs in self._network_objects_by_uid.items()
        }

        network_objects = self.api.session.get(
            f"devices/{device_id}/network_objects"
        ).json()
        for obj in get_api_node(
            network_objects, "network_objects.network_object", listify=True
        ):
            obj = classify_network_object(dict(**obj, device_id=device_id))
            self._network_objects_by_device_id_by_name.setdefault(device_id, {})[
                str(obj["name"])
            ] = obj
            """
            self._network_objects_by_device_id_by_name.setdefault(device_id, {})[
                str(obj["display_name"])
            ] = obj
            """
            self._network_objects_by_uid.setdefault(
                sanitize_uid(obj["uid"]), []
            ).append(obj)

    def _prime_services_cache(self, device_id: int):
        # bust existing cache for device_id
        self._services_by_device_id_by_name[device_id] = {}
        self._services_by_uid = {
            u: [o for o in objs if o.device_id != device_id]
            for u, objs in self._services_by_uid.items()
        }

        services = self.api.session.get(f"devices/{device_id}/services").json()
        for obj in get_api_node(services, "services.service", listify=True):
            obj = classify_service_object(dict(**obj, device_id=device_id))
            self._services_by_device_id_by_name.setdefault(device_id, {})[
                str(obj["name"])
            ] = obj
            self._services_by_uid.setdefault(sanitize_uid(obj["uid"]), []).append(obj)

    def get_shadowing_rules_for_device(
        self: "St", device: str, rules: Iterator[str]
    ) -> List[Tuple[SecurityRule, List[SecurityRule]]]:
        rules = self.api.session.get(
            f"devices/{device}/shadowing_rules",
            params={"shadowed_uids": ",".join(rules)},
        )

        if not rules.ok:
            try:
                msg = rules.json().get("result").get("message")
                rules.raise_for_status()
            except HTTPError as e:
                raise ValueError(
                    f"Unable to get shadowing rules got '{msg}' from API Error: {e}"
                )
        rules_json = (
            rules.json()
            .get("cleanup_set")
            .get("shadowed_rules_cleanup")
            .get("shadowed_rules")
            .get("shadowed_rule")
        )
        result_rules = []
        for rule in rules_json:
            rule_and_shadowing_rules_pair = (
                SecurityRule.kwargify(rule.get("rule")),
                [
                    SecurityRule.kwargify(r)
                    for r in rule.get("shadowing_rules").get("rule")
                ],
            )
            result_rules.append(rule_and_shadowing_rules_pair)
        return result_rules

    def get_network_objects(
        self, device: Union[int, str], cache: Optional[bool] = None
    ):
        if cache is not False and self.cache:
            device_obj = self.get_device(device)
            if device_obj is None:
                raise ValueError(f"Device {device} not found")
            device_id = device_obj.id
            if device_id not in self._network_objects_by_device_id_by_name:
                self._prime_network_objects_cache(device_id)

            objs = list(self._network_objects_by_device_id_by_name[device_id].values())
            for obj in objs:
                obj.device_id = device_id
        return objs

    def get_network_object(
        self,
        name: Optional[str] = None,
        device: Union[int, str, None] = None,
        uid: Optional[str] = None,
        cache=True,
    ) -> NetworkObject:
        device_obj = None
        if device:
            device_obj = self.get_device(device)
            if device_obj is None:
                raise ValueError(f"Device {device} not found")
        if self.cache and cache:
            if uid:
                uid = sanitize_uid(uid)
                if uid not in self._network_objects_by_uid:
                    objs = self.api.session.get(
                        "network_objects/search", params={"filter": "uid", "uid": uid}
                    ).json()

                    for obj_json in get_api_node(
                        objs, "network_objects.network_object", listify=True
                    ):
                        obj = classify_network_object(obj_json)
                        self._network_objects_by_uid.setdefault(
                            sanitize_uid(obj["uid"]), []
                        ).append(obj)
                        self._network_objects_by_device_id_by_name.setdefault(
                            obj["device_id"], {}
                        )[obj["name"]] = obj

                objs = self._network_objects_by_uid.get(uid, [None])
                if len(objs) > 1:
                    if device_obj is None:
                        raise AssertionError(
                            f"More than one object found for uid {uid}, device argument must be passed"
                        )
                    else:
                        for obj in objs:
                            if obj.device_id == device_obj.id:
                                objs = [obj]
                                break
                        else:
                            objs = [None]
                return objs[0]

            elif not name or device_obj is None:
                raise ValueError(
                    "name and device arguments must be passed if uid is None"
                )
            device_id = device_obj.id
            if device_id not in self._network_objects_by_device_id_by_name:
                network_objects = self.api.session.get(
                    f"devices/{device_id}/network_objects"
                ).json()
                for obj_json in get_api_node(
                    network_objects, "network_objects.network_object", listify=True
                ):
                    obj = classify_network_object(obj_json)
                    self._network_objects_by_device_id_by_name.setdefault(
                        device_id, {}
                    )[str(obj["name"])] = obj
                    obj.device_id = device_id
                    self._network_objects_by_uid.setdefault(
                        sanitize_uid(obj["uid"]), []
                    ).append(obj)
            return self._network_objects_by_device_id_by_name[device_id].get(name)
        else:
            raise NotImplementedError(
                "Non-caching mode is not supported...yet"
            )  # pragma: no cover

    def get_services(self, device: Union[int, str], cache: Optional[bool] = None):
        if cache is not False and self.cache:
            device_obj = self.get_device(device)
            if device_obj is None:
                raise ValueError(f"Device {device} not found")
            device_id = device_obj.id
            if device_id not in self._services_by_device_id_by_name:
                self._prime_services_cache(device_id)
            objs = list(self._services_by_device_id_by_name[device_id].values())
            for obj in objs:
                obj.device_id = device_id
        return objs

    def get_service(
        self,
        name: Optional[str] = None,
        device: Union[int, str, None] = None,
        uid: Optional[str] = None,
        cache=True,
    ) -> Service:
        device_obj = None
        if device:
            device_obj = self.get_device(device)
            if device_obj is None:
                raise ValueError(f"Device {device} not found")
        if self.cache and cache:
            if uid:
                uid = sanitize_uid(uid)
                if uid not in self._services_by_uid:
                    params = {"filter": "uid", "uid": uid}

                    if device_obj:
                        params["device_id"] = device_obj.id

                    objs = self.api.session.get("services/search", params=params).json()

                    for obj_json in get_api_node(
                        objs, "services.service", listify=True
                    ):
                        obj = classify_service_object(obj_json)
                        self._services_by_uid.setdefault(
                            sanitize_uid(obj["uid"]), []
                        ).append(obj)

                        self._services_by_device_id_by_name.setdefault(
                            obj.device_id or device_obj.id, {}
                        )[obj["name"]] = obj

                objs = self._services_by_uid.get(uid, [None])
                if len(objs) > 1:
                    if device_obj is None:
                        raise AssertionError(
                            "More than one object found for uid {uid}, device argument must be passed"
                        )
                    else:
                        for obj in objs:
                            if obj.device_id == device_obj.id:
                                objs = [obj]
                                break
                        else:
                            objs = [None]
                return objs[0]

            elif not name or device_obj is None:
                raise ValueError(
                    "name and device arguments must be passed if uid is None"
                )
            device_id = device_obj.id
            if (
                device_id not in self._services_by_device_id_by_name
                or name not in self._services_by_device_id_by_name[device_id]
            ):
                services = self.api.session.get(f"devices/{device_id}/services").json()
                for obj_json in get_api_node(
                    services, "services.service", listify=True
                ):
                    obj = classify_service_object(obj_json)
                    self._services_by_device_id_by_name.setdefault(device_id, {})[
                        str(obj["name"])
                    ] = obj
                    obj.device_id = device_id
                    self._services_by_uid.setdefault(
                        sanitize_uid(obj["uid"]), []
                    ).append(obj)

            return self._services_by_device_id_by_name[device_id].get(name)
        else:
            raise NotImplementedError(
                "Non-caching mode is not supported...yet"
            )  # pragma: no cover

    def _prime_rules_cache(self):
        self._device_rules_dict = {}
        self._revision_rules_dict = {}

    def _transform_rules_response(self, rules_response: Response) -> Iterator:
        if not rules_response.ok:
            try:
                msg = rules_response.text
                rules_response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Got '{msg}' from Error :{e}")

        rules_json = rules_response.json()
        rules_json = get_api_node(rules_json, "rules.rule", listify=True)
        rules = [SecurityRule.kwargify(rule) for rule in rules_json]
        return rules

    def _transform_nat_rules_response(self, nat_rules_response: Response) -> Iterator:
        if not nat_rules_response.ok:
            try:
                msg = nat_rules_response.json().get("result").get("message")
                nat_rules_response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Got '{msg}' from Error: {e}")

        nat_rules_json = nat_rules_response.json()
        nat_rules_json = get_api_node(nat_rules_json, "nat_rule", listify=True)
        nat_rules = [SecurityRule.kwargify(nat_rule) for nat_rule in nat_rules_json]
        return nat_rules

    def _filter_rule_uid(self, rules, rule_uid):
        if rule_uid:
            mat_rules = [rule for rule in rules if uids_match(rule.uid, rule_uid)]
            return mat_rules
        else:
            return rules

    def _get_rules_by_revision(
        self,
        revision: int,
        rule_uid: Optional[str] = None,
        uid: Optional[str] = None,
        documentation: bool = True,
        cache: bool = True,
    ):
        revision_obj = self.get_revision(revision=revision)
        revision_id = revision_obj.id
        if cache and self.cache:
            if not self._revision_rules_dict:
                self._prime_rules_cache()

            if revision_id in self._revision_rules_dict:
                rules = self._revision_rules_dict[revision_id]

                if rule_uid is not None:
                    return self._filter_rule_uid(rules, rule_uid)
                else:
                    return rules
            else:
                rules_response = self.api.get_rules_from_revision_id(
                    revision_id, uid=uid, documentation=documentation
                )
                rules = self._transform_rules_response(rules_response)

                self._revision_rules_dict[revision_id] = rules
                return self._filter_rule_uid(rules, rule_uid)
        else:
            rules_response = self.api.get_rules_from_revision_id(
                revision_id, uid=uid, documentation=documentation
            )
            rules = self._transform_rules_response(rules_response)

            return self._filter_rule_uid(rules, rule_uid)

    def _get_rules_by_device(
        self,
        device: Union[str, int],
        rule_uid: Optional[str] = None,
        uid: Optional[str] = None,
        documentation: bool = True,
        cache: bool = True,
    ):
        device_obj = self.get_device(device)

        if device_obj is None:
            raise ValueError(f"Device {device} not found")

        latest_revision_id = device_obj.latest_revision
        device_id = device_obj.id
        if cache and self.cache:
            if not self._device_rules_dict:
                self._prime_rules_cache()

            if device_id in self._device_rules_dict:
                return self._filter_rule_uid(
                    self._device_rules_dict[device_id], rule_uid
                )

            else:
                rules_response = self.api.get_rules_from_device_id(
                    device_id, uid=uid, documentation=documentation
                )
                rules = self._transform_rules_response(rules_response)

                for rule in rules:
                    rule.device = device_obj

                self._device_rules_dict[device_id] = rules

                if latest_revision_id is not None:
                    self._revision_rules_dict[latest_revision_id] = rules

                if rule_uid:
                    return self._filter_rule_uid(rules, rule_uid)
                else:
                    return rules
        else:
            rules_response = self.api.get_rules_from_device_id(
                device_id, uid=uid, documentation=documentation
            )
            rules = self._transform_rules_response(rules_response)

            for rule in rules:
                rule.device = device_obj

            return rules

    def _get_nat_rules_by_device(self, device: Union[str, int]):
        def _get_response(device_obj, interface_name=None):
            device_id = device_obj.id

            nat_rules_response = self.api.get_nat_rules_from_device_id(
                device_id, input_interface=interface_name
            )
            if not nat_rules_response.ok:
                try:
                    msg = nat_rules_response.json().get("result").get("message")
                    nat_rules_response.raise_for_status()
                except HTTPError as e:
                    raise ValueError(f"got '{msg}' from Error {e}")

            nat_rules = self._transform_nat_rules_response(nat_rules_response)

            for rule in nat_rules:
                rule.device = device_obj

            return nat_rules

        should_iterate_interfaces = False

        device_obj = self.get_device(device)

        if device_obj is None:
            raise ValueError(f"Device {device} not found")

        if device_obj.vendor in [Device.Vendor.CISCO]:
            should_iterate_interfaces = True

        device_id = device_obj.id

        interfaces = None
        rules = []
        if should_iterate_interfaces:
            interfaces = self.get_interfaces(device_id)
            for interface in interfaces:
                iface_nat_rules = _get_response(device_obj, interface.name)
                for rule in iface_nat_rules:
                    rules.append(rule)
            return rules
        else:
            nat_rules = _get_response(device_obj, None)

            for rule in nat_rules:
                rules.append(rule)
            return rules

    def get_nat_rules(self, device: Union[str, int, None] = None) -> List[SecurityRule]:
        if device is None:
            raise NotImplementedError(
                "Current SDK does not support NAT rules for all devices"
            )
        elif device is not None:
            device_obj = self.get_device(device)
            to_return_nat_rules = []
            nat_rules = self._get_nat_rules_by_device(device=device)
            nat_rule_map = {}
            for n in nat_rules:
                nat_rule_map[n.id] = n

            for nat_rule in nat_rule_map.values():
                nat_rule.device = device_obj
                to_return_nat_rules.append(nat_rule)
            return to_return_nat_rules

    def get_rules(
        self,
        device: Union[str, int, None] = None,
        revision: Union[int, None] = None,
        rule_uid: Optional[str] = None,
        uid: Optional[str] = None,
        documentation: bool = True,
        cache: bool = True,
    ) -> List[SecurityRule]:
        match_rules = []
        if device is None and revision is None:
            for device in self.get_devices():
                rules = self._get_rules_by_device(
                    device=device.id,
                    rule_uid=rule_uid,
                    uid=uid,
                    documentation=documentation,
                    cache=cache,
                )
                for rule in rules:
                    rule.device = device

                    if rule_uid is not None and uids_match(rule.uid, rule_uid):
                        match_rules.append(rule)
                    elif rule_uid is None:
                        match_rules.append(rule)
        elif device is not None and revision is not None:
            raise ValueError(
                "You cannot specify both revision and device arguments for the same call"
            )

        elif device is not None:
            rules = self._get_rules_by_device(
                device=device,
                rule_uid=rule_uid,
                uid=uid,
                documentation=documentation,
                cache=cache,
            )
            device_obj = self.get_device(device)
            for rule in rules:
                rule.device = device_obj
                match_rules.append(rule)

        elif revision is not None:
            rules = self._get_rules_by_revision(
                revision=revision,
                rule_uid=rule_uid,
                uid=uid,
                documentation=documentation,
                cache=cache,
            )
            for rule in rules:
                match_rules.append(rule)
        return match_rules

    def get_rule_documentation(
        self: "St", device: Union[str, int], rule: Union[int, SecurityRule]
    ) -> Documentation:
        device_obj = self.get_device(device)
        rule_id = rule.id if isinstance(rule, SecurityRule) else rule
        r = self.api.session.get(
            f"devices/{device_obj.id}/rules/{rule_id}/documentation"
        )
        if not r.ok:
            r.raise_for_status()  # no detail msg in response
        return Documentation.kwargify(r.json()["rule_documentation"])

    def update_rule_documentation(
        self,
        device: Union[str, int],
        rule: Union[int, SecurityRule],
        rule_documentation: Documentation,
    ) -> None:
        if isinstance(device, str):
            device_obj = self.get_device(device)
            device = device_obj.id
        rule_id = rule.id if isinstance(rule, SecurityRule) else rule
        documentation_body = {"rule_documentation": rule_documentation._json}

        r = self.api.session.put(
            f"devices/{device}/rules/{rule_id}/documentation", json=documentation_body
        )

        if not r.ok:
            r.raise_for_status()

    def _prime_revisions_cache(self):
        self._revisions_dict = {}
        self._device_revisions_dict = {}

    def _get_revision_from_cache(self, revision_id: int):
        revision = self._revisions_dict.get(revision_id, None)
        if not revision:
            raise TypeError("No revision found in cache")
        return revision

    def _get_revision_from_server(self, revision_id: int):
        revision_response = self.api.session.get(f"revisions/{revision_id}")
        if not revision_response.ok:
            try:
                msg = (
                    revision_response.json().get("result").get("message")
                    if revision_response.text
                    else f"Generic API Error {revision_response.status_code}"
                )
                revision_response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"got '{msg}' from Error :{e}")

        revision_json = revision_response.json()
        revision_json = get_api_node(revision_json, "revision")
        return Revision.kwargify(revision_json)

    def get_revision(self, revision: int, cache: bool = True) -> Revision:
        if cache and self.cache:
            if not self._revisions_dict:
                self._prime_revisions_cache()
            try:
                revision_obj = self._get_revision_from_cache(revision)
            except TypeError as e:
                try:
                    revision_obj = self._get_revision_from_server(revision)
                except HTTPError as e:
                    raise ValueError(f"got error :{e}")
            self._revisions_dict[revision] = revision_obj
            return revision_obj
        else:
            return self._get_revision_from_server(revision)

    def get_latest_revision(self, device: Union[str, int]):
        device_id = self.get_device(device).id if isinstance(device, str) else device
        revision_response = self.api.session.get(f"devices/{device_id}/latest_revision")
        # API return can not be JSON Decoded - use generic error
        if not revision_response.ok:
            revision_response.raise_for_status()

        revision_json = revision_response.json()
        revision_json = get_api_node(revision_json, "revision")

        revision_obj = Revision.kwargify(revision_json)
        return revision_obj

    def _get_revisions_from_cache(self, device_id: int):
        revisions = self._device_revisions_dict.get(device_id, None)
        if revisions:
            return revisions
        else:
            return False

    def _get_revisions_from_server(self, device_id: int):
        revisions_response = self.api.session.get(f"devices/{device_id}/revisions")
        if not revisions_response.ok:
            revisions_response.raise_for_status()

        revisions_json = revisions_response.json()
        revisions_json = get_api_node(revisions_json, "revision", listify=True)

        revisions = [Revision.kwargify(revision) for revision in revisions_json]
        return revisions

    def get_revisions(self, device: Union[str, int], cache: bool = True):
        device_obj = self.get_device(identifier=device)
        if not device_obj:
            raise ValueError(f"Device {device} not found")
        device_id = device_obj.id

        if cache and self.cache:
            if not self._device_revisions_dict:
                self._prime_revisions_cache()

            revisions = self._get_revisions_from_cache(device_id)
            if revisions:
                return revisions
            else:
                revisions = self._get_revisions_from_server(device_id)
                self._device_revisions_dict[device_id] = revisions
                return revisions
        else:
            return self._get_revisions_from_server(device_id)

    def search_rules(
        self: "St",
        text: Optional[str] = None,
        devices: Union[Union[str, int], List[Union[str, int]]] = None,
        context: Optional[int] = None,
        # The list of known rule search parameters that have been encoded (so
        # far):
        shadowed: Optional[bool] = None,
        expiration_date: Optional[Union[Emptiness, date]] = None,
        certification_expiration_date: Optional[Union[Emptiness, date]] = None,
        comment: Optional[Emptiness] = None,
        # The unknowns (dun dun dun):
        #
        # (N.B. that search params passed by name in the type signature
        # (`shadowed`, etc.) will overwrite any params inside of
        # `search_text_params` (actually, if you try to call the function like:
        # `st.search_rules(shadowed=True, **{"shadowed": True})` it will crash),
        # so please prefer passing search query params by name if you can.)
        **search_text_params: Dict[str, Union[str, bool, List[Union[str, bool]]]],
    ) -> List[SecurityRule]:
        # This function operates in two stages:
        #
        # 1. First it calls the base "/rule_search" endpoint with your given
        # device list (or all devices if no device list was passed) and search
        # queries to see which devices will be sub-queried.
        #
        # 1. Next, it consecutively calls the "/rule_search/{device_id}"
        # endpoint per device, and returns every rule that matches your query.

        # For whatever reason, rule_search supports a format that wants you to
        # put your search text and your other queries all together in the same
        # `search_text` URI parameter. However, actual search `str` *text* must
        # be specified first. So instead of something like this:
        #
        #     ?search_text=my cool search text&shadowed=true&action=accept
        #
        # We have to do this:
        #
        #     ?search_text=my cool search text shadowed:true action:accept
        #
        # N.B.: It seems that the API parses ':' and '%3A' into the same value,
        # so it currently unknown to me how to include a literal `':'` in the
        # text portion of an programmatic hit of this endpoint (without that
        # text portion being treated as a key:value pair).
        devices_cache = {d.id: d for d in self.get_devices()}
        if devices is None:
            devices = devices_cache.keys()
        if not isinstance(devices, Iterable):
            devices = [devices]
        _search_text_params = []
        for k, v in search_text_params.items():
            if k == "uid":
                v = sanitize_uid(v)
            _search_text_params.append(_querify(k, v))
        search_text_params = _search_text_params
        search_text_string = " ".join(search_text_params)
        if expiration_date is not None:
            if isinstance(expiration_date, Emptiness):
                string = f"{expiration_date.value}"
            else:
                string = f":{expiration_date.strftime('%Y%m%d')}"
            search_text_params.append("expirationdate" + string)

        if certification_expiration_date is not None:
            if isinstance(certification_expiration_date, Emptiness):
                string = f"{certification_expiration_date.value}"
            else:
                string = f":{certification_expiration_date.strftime('%Y%m%d')}"
            search_text_params.append("certificationexpirationdate" + string)

        if comment is not None:
            search_text_params.append(f"comment{comment.value}")

        def _chunked_rule_search(devices):
            LOGGER.debug(f"Running chunked rule search for devices: {devices}")

            params = OrderedDict(
                {
                    "devices": ",".join(str(d) for d in devices),
                    "search_text": text + " " if text is not None else "",
                }
            )
            if context:
                params["context"] = context

            params["search_text"] += search_text_string

            if shadowed is not None:
                search_text_params.append(f"shadowed:{_bool(shadowed)}")

            # N.B.: It *is* possible to save one HTTP request here if we only have
            # a single device id in `devices`, as we can skip the `/rule_search`
            # hit and just request `/rule_search/{devices[0]}` immediately, but it
            # wasn't worth the complexity of implementation as `/rule_search` is
            # plenty fast.
            rule_search_info = self.api.session.get("rule_search", params=params)
            if not rule_search_info.ok:
                try:
                    msg = rule_search_info.json().get("result").get("message")
                    rule_search_info.raise_for_status()
                except HTTPError as e:
                    raise ValueError(f"got '{msg}' from API Error: {e}")

            rule_search_info = rule_search_info.json()

            # Walrus, come save me.
            rule_search_info = rule_search_info.get("device_list")
            if rule_search_info is None:
                return
            rule_search_info = rule_search_info.get("device")
            if rule_search_info is None:
                return

            # Save me twice.
            devices = [
                {
                    "rule_count": device_info["rule_count"],
                    "device_id": device_info["device_id"],
                }
                for device_info in rule_search_info
                if device_info.get("device_id") is not None
                and device_info.get("rule_count", 0) > 0
            ]

            return devices

        total_rule_count = 0

        devices = list(devices)  # Turn dict_keys() into list for chunking below
        i = 0
        found_rules = []
        while i < len(devices):
            device_ids = devices[i : i + 50]
            i += 50

            _devices_chunk = _chunked_rule_search(device_ids)

            total_rule_count += sum([d["rule_count"] for d in _devices_chunk])

            for device_info in _devices_chunk:
                device_id = device_info["device_id"]
                device_rule_count = device_info["rule_count"]

                device = devices_cache.get(device_id)
                if device is None:
                    LOGGER.warning(
                        {
                            "message": f"There is no device known to SecureTrack with id {device_id}; perhaps it was deleted? Skipping.",
                            "device": {"id": device_id},
                        }
                    )
                    continue

                # N.B.: API results are 0-based, not one-based. So passing in a
                # `count` of 3000 will return items starting from the 3001st and so
                # forth (passing in 0 will return starting from item #1).
                params = OrderedDict(
                    {"start": 0, "count": 3000, "search_text": search_text_string}
                )
                rules_retrieved_for_this_device = 0

                while rules_retrieved_for_this_device < device_rule_count:
                    rules = self.api.session.get(
                        f"rule_search/{device.id}", params=params
                    )
                    params["start"] += params["count"]

                    if not rules.ok:
                        try:
                            msg = rules.json().get("result").get("message")
                            rules.raise_for_status()
                        except HTTPError as e:
                            raise ValueError(f"got '{msg}' from API error: {e}")
                    rules = rules.json()

                    if rules.get("rules") is None:
                        break
                    if rules["rules"].get("rule") is None:
                        break
                    if rules["rules"].get("count") is None:
                        break

                    for rule in rules["rules"]["rule"]:
                        rule = SecurityRule.kwargify(rule)
                        rule.total_rule_count = total_rule_count
                        rule.device_rule_count = device_rule_count
                        rule.device = device
                        found_rules.append(rule)

                    rules_retrieved_for_this_device += rules["rules"]["count"]
        return found_rules

    def rule_search(self, *args: tuple, **kwargs: dict) -> List[SecurityRule]:
        return self.search_rules(*args, **kwargs)

    def update_documentation(
        self, device_id: int, rule_id: int, rule_doc: Documentation
    ):
        response = self.api.session.put(
            f"devices/{device_id}/rules/{rule_id}/documentation", json=rule_doc._json
        )

        if not response.ok:
            response.raise_for_status()

    def get_device_policies(self, device: Union[int, str]) -> List[BindingPolicy]:
        if isinstance(device, str):
            device_obj = self.get_device(device)
            if not device_obj:
                raise ValueError(f"Cannot find device {device}")

            device_id = device_obj.id
        else:
            device_id = device

        response = self.api.session.get(f"devices/{device_id}/policies")
        if not response.ok:
            response.raise_for_status()

        _json = response.json()

        policies = get_api_node(_json, "policies", listify=True)
        to_return_policies = []
        for policy in policies:
            try:
                policy_obj = BindingPolicy.kwargify(policy)
                to_return_policies.append(policy_obj)
            except Exception as e:  # pragma: no cover
                raise ValueError(
                    f"unable to kwargify policy_json: {policy}, got error: {e}"
                )
        return to_return_policies

    def get_device_policy(self, device: Union[int, str], policy: str) -> BindingPolicy:
        policies = self.get_device_policies(device)

        for policy_obj in policies:
            if policy_obj.name == policy:
                return policy_obj

        raise ValueError("No matching policy found in given device.")

    def get_interfaces(self, device_id: int) -> List[Interface]:
        device_info = self.default.get_device(device_id)

        if device_info and device_info.vendor.name == "CHECKPOINT":
            interfaces = self.api.get_topology_interfaces_from_device_id(device_id)
            base_id = "interface"
        else:
            interfaces = self.api.get_interfaces_from_device_id(device_id)
            base_id = "interfaces.interface"

        if interfaces.status_code == 404:
            raise ValueError(f"Device {device_id} not found")
        elif interfaces.status_code == 400:
            # checkpoint devices unsupported returns 400
            raise ValueError(
                f"CheckPoint Device {device_id} not supported, use topology_interfaces"
            )
        else:
            return [
                Interface.kwargify(d)
                for d in get_api_node(interfaces.json(), base_id, listify=True)
            ]

    def get_bindable_objects(self, device_id: int) -> List[BindableObject]:
        objects = self.api.get_bindable_objects_from_device_id(device_id)
        if objects.status_code == 404:
            raise ValueError(f"Device {device_id} not found")
        else:
            return [
                BindableObject.kwargify(d)
                for d in get_api_node(objects.json(), "bindable_objects", listify=True)
            ]

    def get_topology_interfaces(
        self, device_id: int, is_generic: Optional[int] = 0
    ) -> List[TopologyInterface]:
        interfaces = self.api.get_topology_interfaces_from_device_id(
            device_id, is_generic=is_generic
        )

        return [
            TopologyInterface.kwargify(d)
            for d in get_api_node(interfaces.json(), "interface", listify=True)
        ]

    def get_generic_devices(
        self,
        name: Optional[str] = None,
        context: Optional[int] = None,
        cache: bool = True,
    ) -> List[GenericDevice]:
        if not cache:
            response = self.api.get_generic_devices(name=name, context=context)
            if not response.ok:
                try:
                    msg = response.text
                    response.raise_for_status()
                except HTTPError as e:
                    raise ValueError(
                        f"Got {e}, with Error Message: {msg} from generic_devices API"
                    )
            else:
                generic_devices = get_api_node(
                    response.json(), "generic_devices.device", listify=True
                )
                return [GenericDevice.kwargify(d) for d in generic_devices]
        else:
            if self._generic_devices_cache.is_empty():
                self._prime_generic_devices_cache()

            if name is None:
                return self._generic_devices_cache.get_data()
            else:
                for d in self._generic_devices_cache.get_data():
                    if name == d.name:
                        return d

    def delete_generic_device(
        self, identifier: Union[int, str], update_topology: bool = False
    ) -> None:
        if isinstance(identifier, str):
            if self._generic_devices_cache.is_empty():
                self._prime_generic_devices_cache()

            device = self._generic_devices_index.get(identifier)
            if device is None:
                raise ValueError("Could not find device with specified name")

            identifier = device.id

        response = self.api.delete_generic_device(
            id=identifier, update_topology=update_topology
        )

        if not response.ok:
            try:
                msg = response.text
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"got '{msg}' from API Error: {e}")

    def add_generic_device(
        self,
        name: str,
        configuration: Union[BytesIO, str],
        update_topology: bool = False,
        customer_id: Optional[int] = None,
    ) -> None:
        response = self.api.post_generic_device(
            name=name,
            configuration=configuration,
            update_topology=update_topology,
            customer_id=customer_id,
        )

        if not response.ok:
            try:
                msg = response.text
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"got '{msg}' from API Error: {e}")

    def update_generic_device(
        self,
        id: int,
        name: str,
        configuration: Union[BytesIO, str],
        update_topology: bool = False,
    ) -> None:
        response = self.api.put_generic_device(
            id=id,
            configuration=configuration,
            name=name,
            update_topology=update_topology,
        )

        if not response.ok:
            try:
                msg = response.text
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"got '{msg}' from API Error :{e}")

    def import_generic_device(
        self,
        name: str,
        configuration: Union[BytesIO, str],
        update_topology: bool = False,
        customer_id: Optional[int] = None,
    ):
        if self._generic_devices_cache.is_empty():
            self._prime_generic_devices_cache()

        existing_device = self._generic_devices_index.get(name)

        if existing_device is None:
            return self.add_generic_device(
                name=name,
                configuration=configuration,
                update_topology=update_topology,
                customer_id=customer_id,
            )
        else:
            return self.update_generic_device(
                id=existing_device.id,
                name=name,
                configuration=configuration,
                update_topology=False,
            )

    def sync_topology(self, full_sync: bool = False):
        response = self.api.session.post(
            "topology/synchronize", params={"full_sync": full_sync}
        )

        if response.ok:
            return
        elif response.status_code == 401:
            raise ValueError("Authentication error")
        elif response.status_code == 500:
            raise ValueError("Error synchronizing topology model")
        else:
            response.raise_for_status()

    def get_topology_sync_status(self) -> TopologySyncStatus:
        response = self.api.session.get("topology/synchronize/status")

        if response.ok:
            status = get_api_node(response.json(), "status")
            status = TopologySyncStatus.kwargify(status)
            return status
        elif response.status_code == 401:
            raise ValueError("Authentication error")
        elif response.status_code == 500:
            raise ValueError("Error getting synchronization process")
        else:
            response.raise_for_status()

    def _generic_body(self, type: str, data: Union[dict, List[dict]]) -> dict:
        return {type: data if isinstance(data, typing.List) else [data]}

    def add_generic_interface(self, interface: dict) -> None:
        data = self._generic_body("GenericInterfaces", interface)
        response = self.api.session.post("topology/generic/interface", json=data)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Adding Generic Interface: {e}")

    def add_generic_interfaces(self, interfaces: List[dict]) -> None:
        data = self._generic_body("GenericInterfaces", interfaces)
        response = self.api.session.post("topology/generic/interface", json=data)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Adding Generic Interfaces: {e}")

    def get_generic_interface(self, int_id: Union[int, str]) -> GenericInterface:
        response = self.api.session.get(f"topology/generic/interface/{int_id}")
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Getting Generic Interface: {e}")

        interface = get_api_node(response.json(), "GenericInterface")
        return GenericInterface.kwargify(interface)

    def get_generic_interfaces(
        self, mgmt_id: Union[int, str]
    ) -> List[GenericInterface]:
        response = self.api.session.get(f"topology/generic/interface/mgmt/{mgmt_id}")
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Getting Generic Interfaces: {e}")

        return [
            GenericInterface.kwargify(d)
            for d in get_api_node(response.json(), "GenericInterfaces", listify=True)
        ]

    def update_generic_interface(self, interface: dict) -> None:
        data = self._generic_body("GenericInterfaces", interface)
        response = self.api.session.put("topology/generic/interface", json=data)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Updating Generic Interface: {e}")

    def update_generic_interfaces(self, interfaces: List[dict]) -> None:
        data = self._generic_body("GenericInterfaces", interfaces)
        response = self.api.session.put("topology/generic/interface", json=data)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Updating Generic Interfaces: {e}")

    def delete_generic_interface(self, int_id: Union[int, str]) -> None:
        response = self.api.session.delete(f"topology/generic/interface/{int_id}")
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Deleting Generic Interface: {e}")

    def delete_generic_interfaces(self, mgmt_id: Union[int, str]) -> None:
        response = self.api.session.delete(f"topology/generic/interface/mgmt/{mgmt_id}")
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Deleting Generic Interfaces: {e}")

    def add_generic_route(self, route: dict) -> None:
        data = self._generic_body("GenericRoutes", route)
        response = self.api.session.post("topology/generic/route", json=data)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Adding Generic Route: {e}")

    def add_generic_routes(self, routes: List[dict]) -> None:
        data = self._generic_body("GenericRoutes", routes)
        response = self.api.session.post("topology/generic/route", json=data)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Adding Generic Routes: {e}")

    def get_generic_route(self, int_id: Union[int, str]) -> GenericRoute:
        response = self.api.session.get(f"topology/generic/route/{int_id}")
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Getting Generic Route: {e}")

        route = get_api_node(response.json(), "GenericRoute")
        return GenericRoute.kwargify(route)

    def get_generic_routes(self, mgmt_id: Union[int, str]) -> List[GenericRoute]:
        response = self.api.session.get(f"topology/generic/route/mgmt/{mgmt_id}")
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Getting Generic Routes: {e}")

        return [
            GenericRoute.kwargify(d)
            for d in get_api_node(response.json(), "GenericRoutes", listify=True)
        ]

    def update_generic_route(self, route: dict) -> None:
        data = self._generic_body("GenericRoutes", route)
        response = self.api.session.put("topology/generic/route", json=data)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Updating Generic Route: {e}")

    def update_generic_routes(self, routes: List[dict]) -> None:
        data = self._generic_body("GenericRoutes", routes)
        response = self.api.session.put("topology/generic/route", json=data)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Updating Generic Routes: {e}")

    def delete_generic_route(self, int_id: Union[int, str]) -> None:
        response = self.api.session.delete(f"topology/generic/route/{int_id}")
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Deleting Generic Route: {e}")

    def delete_generic_routes(self, mgmt_id: Union[int, str]) -> None:
        response = self.api.session.delete(f"topology/generic/route/mgmt/{mgmt_id}")
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Deleting Generic Routes: {e}")

    def add_generic_vpn(self, vpn: dict) -> None:
        data = self._generic_body("GenericVpns", vpn)
        response = self.api.session.post("topology/generic/vpn", json=data)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Adding Generic Vpn: {e}")

    def add_generic_vpns(self, vpns: List[dict]) -> None:
        data = self._generic_body("GenericVpns", vpns)
        response = self.api.session.post("topology/generic/vpn", json=data)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Adding Generic Vpns: {e}")

    def get_generic_vpn(self, int_id: Union[int, str]) -> GenericVpn:
        response = self.api.session.get(f"topology/generic/vpn/{int_id}")
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Getting Generic Vpn: {e}")

        vpn = get_api_node(response.json(), "GenericVpn")
        return GenericVpn.kwargify(vpn)

    def get_generic_vpns(self, device_id: Union[int, str]) -> List[GenericVpn]:
        response = self.api.session.get(f"topology/generic/vpn/device/{device_id}")
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Getting Generic Vpns: {e}")

        return [
            GenericVpn.kwargify(d)
            for d in get_api_node(response.json(), "GenericVpns", listify=True)
        ]

    def update_generic_vpn(self, vpn: dict) -> None:
        data = self._generic_body("GenericVpns", vpn)
        response = self.api.session.put("topology/generic/vpn", json=data)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Updating Generic Vpn: {e}")

    def update_generic_vpns(self, vpns: List[dict]) -> None:
        data = self._generic_body("GenericVpns", vpns)
        response = self.api.session.put("topology/generic/vpn", json=data)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Updating Generic Vpns: {e}")

    def delete_generic_vpn(self, int_id: Union[int, str]) -> None:
        response = self.api.session.delete(f"topology/generic/vpn/{int_id}")
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Deleting Generic Vpn: {e}")

    def delete_generic_vpns(self, device_id: Union[int, str]) -> None:
        response = self.api.session.delete(f"topology/generic/vpn/device/{device_id}")
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Deleting Generic Vpns: {e}")

    def add_generic_transparent_firewalls(self, firewalls: List[dict]) -> None:
        data = self._generic_body("TransparentFirewalls", firewalls)
        response = self.api.session.post("topology/generic/transparentfw", json=data)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Adding Generic Transparent Firewalls: {e}")

    def get_generic_transparent_firewalls(
        self, device_id: Union[int, str]
    ) -> List[GenericTransparentFirewall]:
        response = self.api.session.get(
            f"topology/generic/transparentfw/device/{device_id}"
        )
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Getting Generic Transparent Firewalls: {e}")

        return [
            GenericTransparentFirewall.kwargify(d)
            for d in get_api_node(response.json(), "TransparentFirewalls", listify=True)
        ]

    def update_generic_transparent_firewalls(self, firewalls: List[dict]) -> None:
        data = self._generic_body("TransparentFirewalls", firewalls)
        response = self.api.session.put("topology/generic/transparentfw", json=data)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Updating Generic Transparent Firewalls: {e}")

    def delete_generic_transparent_firewall(
        self, layer_2_data_id: Union[int, str]
    ) -> None:
        response = self.api.session.delete(
            f"topology/generic/transparentfw/{layer_2_data_id}"
        )
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Deleting Generic Transparent Firewall: {e}")

    def delete_generic_transparent_firewalls(self, device_id: Union[int, str]) -> None:
        response = self.api.session.delete(
            f"topology/generic/transparentfw/device/{device_id}"
        )
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Deleting Generic Transparent Firewalls: {e}")

    def add_generic_ignored_interfaces(self, interfaces: List[dict]) -> None:
        data = self._generic_body("IgnoredInterfaces", interfaces)
        response = self.api.session.post("topology/generic/ignoredinterface", json=data)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Adding Generic Ignored Interfaces: {e}")

    def get_generic_ignored_interfaces(
        self, mgmt_id: Union[int, str]
    ) -> List[GenericIgnoredInterface]:
        response = self.api.session.get(
            f"topology/generic/ignoredinterface/mgmt/{mgmt_id}"
        )
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Getting Generic Ignored Interfaces: {e}")

        return [
            GenericIgnoredInterface.kwargify(d)
            for d in get_api_node(response.json(), "IgnoredInterfaces", listify=True)
        ]

    def delete_generic_ignored_interfaces(self, mgmt_id: Union[int, str]) -> None:
        response = self.api.session.delete(
            f"topology/generic/ignoredinterface/mgmt/{mgmt_id}"
        )
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Deleting Generic Ignored Interfaces: {e}")

    def add_generic_interface_customer(self, interface_customer: dict) -> None:
        data = self._generic_body("InterfaceCustomerTag", interface_customer)
        response = self.api.session.post(
            "topology/generic/interfacecustomer", json=data
        )
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Adding Generic Interface Customer Tag: {e}")

    def add_generic_interface_customers(self, interface_customers: List[dict]) -> None:
        data = self._generic_body("InterfaceCustomerTags", interface_customers)
        response = self.api.session.post(
            "topology/generic/interfacecustomer", json=data
        )
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Adding Generic Interface Customer Tags: {e}")

    def get_generic_interface_customer(
        self, int_cust_id: Union[int, str]
    ) -> GenericInterfaceCustomer:
        response = self.api.session.get(
            f"topology/generic/interfacecustomer/{int_cust_id}"
        )
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Getting Generic Interface Customer Tag: {e}")

        interface_customer = get_api_node(response.json(), "InterfaceCustomerTag")
        return GenericInterfaceCustomer.kwargify(interface_customer)

    def get_generic_interface_customers(
        self, device_id: Union[int, str]
    ) -> List[GenericInterfaceCustomer]:
        response = self.api.session.get(
            f"topology/generic/interfacecustomer/device/{device_id}"
        )
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Getting Generic Interface Customer Tags: {e}")

        return [
            GenericInterfaceCustomer.kwargify(d)
            for d in get_api_node(
                response.json(), "InterfaceCustomerTags", listify=True
            )
        ]

    def update_generic_interface_customer(self, interface_customer: dict) -> None:
        data = self._generic_body("InterfaceCustomerTag", interface_customer)
        response = self.api.session.put("topology/generic/interfacecustomer", json=data)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Updating Generic Interface Customer Tag: {e}")

    def update_generic_interface_customers(
        self, interface_customers: List[dict]
    ) -> None:
        data = self._generic_body("InterfaceCustomerTags", interface_customers)
        response = self.api.session.put("topology/generic/interfacecustomer", json=data)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Updating Generic Interface Customer Tag: {e}")

    def delete_generic_interface_customer(self, int_cust_id: Union[int, str]) -> None:
        response = self.api.session.delete(
            f"topology/generic/interfacecustomer/{int_cust_id}"
        )
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Deleting Generic Interface Customer Tag: {e}")

    def delete_generic_interface_customers(self, device_id: Union[int, str]) -> None:
        response = self.api.session.delete(
            f"topology/generic/interfacecustomer/device/{device_id}"
        )
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Deleting Generic Interface Customer Tags: {e}")

    def add_join_cloud(self, join_cloud: dict) -> None:
        data = self._generic_body("JoinCloud", join_cloud)
        response = self.api.session.post("topology/join/clouds", json=data)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Adding Join Cloud: {e}")

    def get_join_cloud(self, cloud_id: Union[int, str]) -> JoinCloud:
        response = self.api.session.get(f"topology/join/clouds/{cloud_id}")
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Getting Join Cloud: {e}")
        return JoinCloud.kwargify(response.json())

    def update_join_cloud(self, join_cloud: dict) -> None:
        data = self._generic_body("JoinCloud", join_cloud)
        response = self.api.session.put("topology/join/clouds", json=data)
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Updating Join Cloud: {e}")

    def delete_join_cloud(self, cloud_id: Union[int, str]) -> None:
        response = self.api.session.delete(f"topology/join/clouds/{cloud_id}")
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as e:
                raise ValueError(f"Error Deleting Join Cloud: {e}")
