"""Binary sensor platform for integration_blueprint."""
import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import BINARY_SENSOR, BINARY_SENSOR_DEVICE_CLASS, DEFAULT_NAME, DOMAIN
from .entity import TPLinkESSEntity

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    binary_sensors = []
    limit = coordinator.data.get("num_ports")["num_ports"]
    
    i = 0
    while i < limit:
        binary_sensors.append(
            TPLinkESSBinarySensor(i, coordinator, entry)
        )
        i = i + 1
    async_add_devices(binary_sensors, False)


class TPLinkESSBinarySensor(TPLinkESSEntity, BinarySensorEntity):
    """TPLink ESS binary_sensor class."""

    def __init__(self, port: int, coordinator: DataUpdateCoordinator, config: ConfigEntry) -> None:
        """Initialize."""
        super().__init__(coordinator, config)
        self.coordinator = coordinator
        self._config = config
        self._port = port
        self._data = coordinator.data.get("stats")["stats"][port]
        self._name = self._data["Port"]

        self._attr_name = f"Port {self._name}"
        self._attr_unique_id = f"port{port}_{self._config.entry_id}"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return BINARY_SENSOR_DEVICE_CLASS

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return self._data["Link Status Raw"]

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if "stats" in self.coordinator.data.get("stats"):
            return True
        return False

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._data
