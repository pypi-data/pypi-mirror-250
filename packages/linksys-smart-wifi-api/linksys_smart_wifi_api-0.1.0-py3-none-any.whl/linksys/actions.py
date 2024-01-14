from enum import Enum


class JNAPAction(Enum):
    CHECK_ADMIN_PASSWORD = "http://linksys.com/jnap/core/CheckAdminPassword"
    HAS_DEFAULT_PASSWORD = "http://linksys.com/jnap/core/IsAdminPasswordDefault"
    GET_DEVICE_INFO = "http://linksys.com/jnap/core/GetDeviceInfo"

    START_PING = "http://linksys.com/jnap/diagnostics/StartPing"
    STOP_PING = "http://linksys.com/jnap/diagnostics/StopPing"
    GET_PING_STATUS = "http://linksys.com/jnap/diagnostics/GetPingStatus"

    START_TRACEROUTE = "http://linksys.com/jnap/diagnostics/StartTraceroute"
    STOP_TRACEROUTE = "http://linksys.com/jnap/diagnostics/StopTraceroute"
    GET_TRACEROUTE_STATUS = "http://linksys.com/jnap/diagnostics/GetTracerouteStatus"

    GET_LAN_SETTINGS = "http://linksys.com/jnap/router/GetLANSettings"
    GET_DEVICE_LIST = "http://linksys.com/jnap/core/Transaction"

    GET_USERS = "http://linksys.com/jnap/storage/GetUsers"  # not used?
