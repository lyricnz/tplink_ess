"""Entity class"""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

DOMAIN = "tplink_ess"
MANUFACTURER = "TPLink"


@dataclass
class TPLinkSensorEntityDescription(SensorEntityDescription):
    """Class describing TPLinkESS sensor entities."""

    port: int | None = None


@dataclass
class TPLinkBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Class describing TPLinkESS binary sensor entities."""

    port: int | None = None


class TPLinkESSEntity(CoordinatorEntity):
    """Representation of a TPLink Easy Smart Switch."""

    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator)
        self.config_entry = config_entry

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": str(self.coordinator.data.get("hostname")["hostname"]),
            "model": str(self.coordinator.data.get("hostname")["hardware"]),
            "manufacturer": MANUFACTURER,
            "sw_version": str(self.coordinator.data.get("hostname")["firmware"]),
            "configuration_url": f"http://{self.coordinator.data.get('hostname')['ip_addr']}",
            "connections": {(DOMAIN, self.config_entry.entry_id)},
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success
