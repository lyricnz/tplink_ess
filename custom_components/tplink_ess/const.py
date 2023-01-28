"""Constants for tplink_ess."""
from typing import Final

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.helpers.entity import EntityCategory

from .entity import TPLinkBinarySensorEntityDescription

# Base component constants
NAME = "TPLink ESS"
DOMAIN = "tplink_ess"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.0"
ISSUE_URL = "https://github.com/lyricnz/tplink_ess/issues"
MANUFACTURER = "TPLink"
ICON = "mdi:format-quote-close"

# Platforms
PLATFORMS = ["binary_sensor", "sensor"]

# Defaults
DEFAULT_NAME = DOMAIN

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""

BINARY_SENSORS: Final[dict[str, TPLinkBinarySensorEntityDescription]] = {
    "qos": TPLinkBinarySensorEntityDescription(
        name="QoS",
        key="qos1",
        device_class=BinarySensorDeviceClass.RUNNING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "loop_prevention": TPLinkBinarySensorEntityDescription(
        name="Loop Prevention",
        key="loop_prev",
        device_class=BinarySensorDeviceClass.RUNNING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    "dhcp": TPLinkBinarySensorEntityDescription(
        name="DHCP",
        key="dhcp",
        device_class=BinarySensorDeviceClass.RUNNING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
}
