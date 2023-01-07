"""BlueprintEntity class"""
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER


class TPLinkESSEntity(CoordinatorEntity):
    """Representation of a TPLink Easy Smart Switch."""
    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator)
        self.config_entry = config_entry

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": str(self.coordinator.data.get("hostname")),
            "model": str(self.coordinator.data.get("hardware")),
            "manufacturer": MANUFACTURER,
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "id": str(self.coordinator.data.get("mac")),
            "integration": DOMAIN,
        }
