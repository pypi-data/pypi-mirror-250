from dataclasses import dataclass, field
from enum import Enum

from dataclasses_json import LetterCase, Undefined, config, dataclass_json, DataClassJsonMixin


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class KnownInterface(DataClassJsonMixin):
    class Type(Enum):
        WIRELESS = "Wireless"
        UNKNOWN = "Unknown"

    mac_address: str
    interface_type: Type
    band: str | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Connection(DataClassJsonMixin):
    mac_address: str
    ip_address: str
    ipv6_address: str | None = None
    parent_device_id: str | None = field(default=None, metadata=config(field_name="parentDeviceID"))


@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.EXCLUDE)
@dataclass
class Device(DataClassJsonMixin):
    id_: str = field(metadata=config(field_name="deviceID"))
    name: str | None = field(default=None, metadata=config(field_name="friendlyName"))
    last_change_revision: int = 0
    is_authority: bool = False
    known_interfaces: list[KnownInterface] = field(default_factory=list)
    connections: list[Connection] = field(default_factory=list)

    @property
    def is_connected(self) -> bool:
        return bool(self.connections)

    @property
    def mac_address(self) -> str | None:
        return next((i.mac_address for i in self.known_interfaces), None)


class Service(Enum):
    # from core/GetDeviceInfo -> services
    CORE = "http://linksys.com/jnap/core/Core"
    CORE2 = "http://linksys.com/jnap/core/Core2"
    CORE3 = "http://linksys.com/jnap/core/Core3"
    CORE4 = "http://linksys.com/jnap/core/Core4"
    CORE5 = "http://linksys.com/jnap/core/Core5"
    CORE6 = "http://linksys.com/jnap/core/Core6"
    COREISP = "http://linksys.com/jnap/core/CoreISP"
    DDNS = "http://linksys.com/jnap/ddns/DDNS"
    DDNS2 = "http://linksys.com/jnap/ddns/DDNS2"
    DDNS3 = "http://linksys.com/jnap/ddns/DDNS3"
    DDNS4 = "http://linksys.com/jnap/ddns/DDNS4"
    DEVICELIST = "http://linksys.com/jnap/devicelist/DeviceList"
    DEVICELIST2 = "http://linksys.com/jnap/devicelist/DeviceList2"
    DEVICELIST4 = "http://linksys.com/jnap/devicelist/DeviceList4"
    DEVICELIST5 = "http://linksys.com/jnap/devicelist/DeviceList5"
    DEVICELIST6 = "http://linksys.com/jnap/devicelist/DeviceList6"
    DEVICELIST7 = "http://linksys.com/jnap/devicelist/DeviceList7"
    DEVICEPREAUTHORIZATION = "http://linksys.com/jnap/devicepreauthorization/DevicePreauthorization"
    DIAGNOSTICS = "http://linksys.com/jnap/diagnostics/Diagnostics"
    DIAGNOSTICS2 = "http://linksys.com/jnap/diagnostics/Diagnostics2"
    DIAGNOSTICS3 = "http://linksys.com/jnap/diagnostics/Diagnostics3"
    DIAGNOSTICS6 = "http://linksys.com/jnap/diagnostics/Diagnostics6"
    DIAGNOSTICS7 = "http://linksys.com/jnap/diagnostics/Diagnostics7"
    DIAGNOSTICS8 = "http://linksys.com/jnap/diagnostics/Diagnostics8"
    RELIABILITY = "http://linksys.com/jnap/diagnostics/Reliability"
    DYNAMICPORTFORWARDING = "http://linksys.com/jnap/dynamicportforwarding/DynamicPortForwarding"
    DYNAMICPORTFORWARDING2 = "http://linksys.com/jnap/dynamicportforwarding/DynamicPortForwarding2"
    DYNAMICSESSION = "http://linksys.com/jnap/dynamicsession/DynamicSession"
    DYNAMICSESSION2 = "http://linksys.com/jnap/dynamicsession/DynamicSession2"
    FIREWALL = "http://linksys.com/jnap/firewall/Firewall"
    FIREWALL2 = "http://linksys.com/jnap/firewall/Firewall2"
    FIRMWAREUPDATE = "http://linksys.com/jnap/firmwareupdate/FirmwareUpdate"
    FIRMWAREUPDATE2 = "http://linksys.com/jnap/firmwareupdate/FirmwareUpdate2"
    GUESTNETWORK = "http://linksys.com/jnap/guestnetwork/GuestNetwork"
    GUESTNETWORK2 = "http://linksys.com/jnap/guestnetwork/GuestNetwork2"
    GUESTNETWORK3 = "http://linksys.com/jnap/guestnetwork/GuestNetwork3"
    GUESTNETWORK4 = "http://linksys.com/jnap/guestnetwork/GuestNetwork4"
    GUESTNETWORK5 = "http://linksys.com/jnap/guestnetwork/GuestNetwork5"
    GUESTNETWORKAUTHENTICATION = "http://linksys.com/jnap/guestnetwork/GuestNetworkAuthentication"
    HEALTHCHECKMANAGER = "http://linksys.com/jnap/healthcheck/HealthCheckManager"
    HEALTHCHECKMANAGER2 = "http://linksys.com/jnap/healthcheck/HealthCheckManager2"
    HTTPPROXY = "http://linksys.com/jnap/httpproxy/HttpProxy"
    HTTPPROXY2 = "http://linksys.com/jnap/httpproxy/HttpProxy2"
    LOCALE = "http://linksys.com/jnap/locale/Locale"
    LOCALE2 = "http://linksys.com/jnap/locale/Locale2"
    LOCALE3 = "http://linksys.com/jnap/locale/Locale3"
    MACFILTER = "http://linksys.com/jnap/macfilter/MACFilter"
    NETWORKCONNECTIONS = "http://linksys.com/jnap/networkconnections/NetworkConnections"
    NETWORKCONNECTIONS2 = "http://linksys.com/jnap/networkconnections/NetworkConnections2"
    NETWORKCONNECTIONS3 = "http://linksys.com/jnap/networkconnections/NetworkConnections3"
    AUTOONBOARDING = "http://linksys.com/jnap/nodes/autoonboarding/AutoOnboarding"
    BLUETOOTH = "http://linksys.com/jnap/nodes/bluetooth/Bluetooth"
    BLUETOOTH2 = "http://linksys.com/jnap/nodes/bluetooth/Bluetooth2"
    BTSMARTCONNECT = "http://linksys.com/jnap/nodes/btsmartconnect/BTSmartConnect"
    BTSMARTCONNECT2 = "http://linksys.com/jnap/nodes/btsmartconnect/BTSmartConnect2"
    BTSMARTCONNECT3 = "http://linksys.com/jnap/nodes/btsmartconnect/BTSmartConnect3"
    NODES_DIAGNOSTICS = "http://linksys.com/jnap/nodes/diagnostics/Diagnostics"
    NODES_DIAGNOSTICS2 = "http://linksys.com/jnap/nodes/diagnostics/Diagnostics2"
    NODES_DIAGNOSTICS3 = "http://linksys.com/jnap/nodes/diagnostics/Diagnostics3"
    DIAGNOSTICS5 = "http://linksys.com/jnap/nodes/diagnostics/Diagnostics5"
    NODES_FIRMWAREUPDATE = "http://linksys.com/jnap/nodes/firmwareupdate/FirmwareUpdate"
    NODESNETWORKCONNECTIONS = (
        "http://linksys.com/jnap/nodes/networkconnections/NodesNetworkConnections"
    )
    NOTIFICATION = "http://linksys.com/jnap/nodes/notification/Notification"
    SETUP = "http://linksys.com/jnap/nodes/setup/Setup"
    SETUP2 = "http://linksys.com/jnap/nodes/setup/Setup2"
    SETUP3 = "http://linksys.com/jnap/nodes/setup/Setup3"
    SETUP4 = "http://linksys.com/jnap/nodes/setup/Setup4"
    SETUP5 = "http://linksys.com/jnap/nodes/setup/Setup5"
    SETUP6 = "http://linksys.com/jnap/nodes/setup/Setup6"
    SETUP7 = "http://linksys.com/jnap/nodes/setup/Setup7"
    SETUP8 = "http://linksys.com/jnap/nodes/setup/Setup8"
    SMARTCONNECT = "http://linksys.com/jnap/nodes/smartconnect/SmartConnect"
    SMARTCONNECT2 = "http://linksys.com/jnap/nodes/smartconnect/SmartConnect2"
    SMARTCONNECT3 = "http://linksys.com/jnap/nodes/smartconnect/SmartConnect3"
    SMARTCONNECT4 = "http://linksys.com/jnap/nodes/smartconnect/SmartConnect4"
    SMARTMODE = "http://linksys.com/jnap/nodes/smartmode/SmartMode"
    SMARTMODE2 = "http://linksys.com/jnap/nodes/smartmode/SmartMode2"
    TOPOLOGYOPTIMIZATION = "http://linksys.com/jnap/nodes/topologyoptimization/TopologyOptimization"
    TOPOLOGYOPTIMIZATION2 = (
        "http://linksys.com/jnap/nodes/topologyoptimization/TopologyOptimization2"
    )
    OWNEDNETWORK = "http://linksys.com/jnap/ownednetwork/OwnedNetwork"
    OWNEDNETWORK2 = "http://linksys.com/jnap/ownednetwork/OwnedNetwork2"
    PARENTALCONTROL = "http://linksys.com/jnap/parentalcontrol/ParentalControl"
    PARENTALCONTROL2 = "http://linksys.com/jnap/parentalcontrol/ParentalControl2"
    POWERTABLE = "http://linksys.com/jnap/powertable/PowerTable"
    QOS = "http://linksys.com/jnap/qos/QoS"
    QOS2 = "http://linksys.com/jnap/qos/QoS2"
    QOS3 = "http://linksys.com/jnap/qos/QoS3"
    CALIBRATION = "http://linksys.com/jnap/qos/calibration/Calibration"
    ROUTER = "http://linksys.com/jnap/router/Router"
    ROUTER10 = "http://linksys.com/jnap/router/Router10"
    ROUTER11 = "http://linksys.com/jnap/router/Router11"
    ROUTER3 = "http://linksys.com/jnap/router/Router3"
    ROUTER4 = "http://linksys.com/jnap/router/Router4"
    ROUTER5 = "http://linksys.com/jnap/router/Router5"
    ROUTER6 = "http://linksys.com/jnap/router/Router6"
    ROUTER7 = "http://linksys.com/jnap/router/Router7"
    ROUTER8 = "http://linksys.com/jnap/router/Router8"
    ROUTER9 = "http://linksys.com/jnap/router/Router9"
    ROUTERLEDS = "http://linksys.com/jnap/routerleds/RouterLEDs"
    ROUTERLEDS2 = "http://linksys.com/jnap/routerleds/RouterLEDs2"
    ROUTERLOG = "http://linksys.com/jnap/routerlog/RouterLog"
    ROUTERLOG2 = "http://linksys.com/jnap/routerlog/RouterLog2"
    ROUTERMANAGEMENT = "http://linksys.com/jnap/routermanagement/RouterManagement"
    ROUTERMANAGEMENT2 = "http://linksys.com/jnap/routermanagement/RouterManagement2"
    ROUTERMANAGEMENT3 = "http://linksys.com/jnap/routermanagement/RouterManagement3"
    ROUTERSTATUS = "http://linksys.com/jnap/routerstatus/RouterStatus"
    ROUTERSTATUS2 = "http://linksys.com/jnap/routerstatus/RouterStatus2"
    ROUTERUPNP = "http://linksys.com/jnap/routerupnp/RouterUPnP"
    ROUTERUPNP2 = "http://linksys.com/jnap/routerupnp/RouterUPnP2"
    SMARTCONNECTCLIENT = "http://linksys.com/jnap/smartconnect/SmartConnectClient"
    SMARTCONNECTCLIENT2 = "http://linksys.com/jnap/smartconnect/SmartConnectClient2"
    SETTINGS = "http://linksys.com/jnap/ui/Settings"
    SETTINGS2 = "http://linksys.com/jnap/ui/Settings2"
    SETTINGS3 = "http://linksys.com/jnap/ui/Settings3"
    ADVANCEDWIRELESSAP = "http://linksys.com/jnap/wirelessap/AdvancedWirelessAP"
    ADVANCEDWIRELESSAP2 = "http://linksys.com/jnap/wirelessap/AdvancedWirelessAP2"
    AIRTIMEFAIRNESS = "http://linksys.com/jnap/wirelessap/AirtimeFairness"
    DYNAMICFREQUENCYSELECTION = "http://linksys.com/jnap/wirelessap/DynamicFrequencySelection"
    WPSSERVER = "http://linksys.com/jnap/wirelessap/WPSServer"
    WPSSERVER2 = "http://linksys.com/jnap/wirelessap/WPSServer2"
    WPSSERVER3 = "http://linksys.com/jnap/wirelessap/WPSServer3"
    WPSSERVER4 = "http://linksys.com/jnap/wirelessap/WPSServer4"
    WPSSERVER5 = "http://linksys.com/jnap/wirelessap/WPSServer5"
    WIRELESSAP = "http://linksys.com/jnap/wirelessap/WirelessAP"
    WIRELESSAP2 = "http://linksys.com/jnap/wirelessap/WirelessAP2"
    WIRELESSAP4 = "http://linksys.com/jnap/wirelessap/WirelessAP4"
    ADVANCEDQUALCOMM = "http://linksys.com/jnap/wirelessap/qualcomm/AdvancedQualcomm"
    WIRELESSSCHEDULER = "http://linksys.com/jnap/wirelessscheduler/WirelessScheduler"
    WIRELESSSCHEDULER2 = "http://linksys.com/jnap/wirelessscheduler/WirelessScheduler2"
    XCONNECT = "http://linksys.com/jnap/xconnect/XConnect"


@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.EXCLUDE)
@dataclass
class DeviceInfo(DataClassJsonMixin):
    manufacturer: str
    model_number: str
    hardware_version: str
    description: str
    serial_number: str
    firmware_version: str
    firmware_date: str
    services: list[Service]
