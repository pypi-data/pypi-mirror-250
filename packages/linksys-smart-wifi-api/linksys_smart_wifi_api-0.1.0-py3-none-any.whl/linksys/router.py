from base64 import b64encode
from typing import TYPE_CHECKING, Any, Type

import requests

from .types import Device, DeviceInfo

if TYPE_CHECKING:
    from .actions import JNAPAction


JSONType = dict[str, Any] | list[Any] | int | str | float | bool | None


_DEFAULT_HEADERS = {
    "Content-Type": "application/json; charset=UTF-8",
    "Accept": "application/json",
}


class Linksys:
    def __init__(self, router_url: str, password: str, *, username: str = "admin") -> None:
        self.router_url = f"http://{router_url}".removesuffix("/")

        authentication_token = b64encode(f"{username}:{password}".encode()).decode()
        self._session = requests.Session()
        self._session.headers.update(
            {
                **_DEFAULT_HEADERS,
                "X-JNAP-Authorization": f"Basic {authentication_token}",
            }
        )

    def close(self) -> None:
        self._session.close()

    def _do_action(self, action: "JNAPAction", payload: JSONType = None) -> dict[str, Any]:
        payload = payload or {}
        r = self._session.post(
            f"{self.router_url}/JNAP/", json=payload, headers={"X-JNAP-Action": action.value}
        )
        r.raise_for_status()
        return r.json()

    def get_device_list(self) -> list[Device]:
        content = self._do_action(
            JNAPAction.GET_DEVICE_LIST,
            payload=[
                {
                    "action": "http://linksys.com/jnap/devicelist/GetDevices3",
                    "request": {"sinceRevision": 0},
                }
            ],
        )
        if content["result"] == "OK":
            devices = content["responses"][0]["output"]["devices"]
            return Device.schema().load(devices, many=True)
        return []

    def check_admin_password(self) -> bool:
        return self._do_action(JNAPAction.CHECK_ADMIN_PASSWORD)["result"] == "OK"

    def has_default_password(self) -> bool:
        return self._do_action(JNAPAction.HAS_DEFAULT_PASSWORD)["output"]["isAdminPasswordDefault"]

    def get_device_info(self) -> DeviceInfo:
        content = self._do_action(JNAPAction.GET_DEVICE_INFO)["output"]
        return DeviceInfo.schema().load(content)
