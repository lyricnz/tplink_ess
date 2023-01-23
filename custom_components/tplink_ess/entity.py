"""Entity class"""
from homeassistant.const import CONF_MAC
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER


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
            "name": str(self.coordinator.data.get(CONF_MAC)),
            "model": str(self.coordinator.data.get("hostname")["type"]),
            "manufacturer": MANUFACTURER,
            "sw_version": str(self.coordinator.data.get("hostname")["firmware"]),
            "configuration_url": f"http://{self.coordinator.data.get('hostname')['ip_addr']}",
            "connections": {(DOMAIN, self.config_entry.entry_id)}
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "id": str(self.coordinator.data.get(CONF_MAC)),
            "integration": DOMAIN,
        }
