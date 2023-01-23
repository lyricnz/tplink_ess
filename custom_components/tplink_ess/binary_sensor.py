"""Binary sensor platform for integration_blueprint."""
import logging

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import (DataUpdateCoordinator)

from .const import BINARY_SENSOR_DEVICE_CLASS, DOMAIN
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
            TPLinkESSBinarySensor(i, None, coordinator, entry)
        )
        i = i + 1

    # one off binary sensors
    binary_sensors.append(TPLinkESSBinarySensor(None, "qos1", coordinator, entry))
    binary_sensors.append(TPLinkESSBinarySensor(None, "loop_prev", coordinator, entry))
    binary_sensors.append(TPLinkESSBinarySensor(None, "dhcp", coordinator, entry))
    
    async_add_devices(binary_sensors, False)


class TPLinkESSBinarySensor(TPLinkESSEntity, BinarySensorEntity):
    """TPLink ESS binary_sensor class."""

    def __init__(self, port: int | None, key: str | None, coordinator: DataUpdateCoordinator, config: ConfigEntry) -> None:
        """Initialize."""
        super().__init__(coordinator, config)
        self.coordinator = coordinator
        self._config = config
        self._port = None
        self._key = None
        if port is not None:
            self._data = coordinator.data.get("stats")["stats"][port]
            self._port = port
            self._name = self._data["Port"]
            self._attr_name = f"Port {self._name}"
            self._attr_unique_id = f"port{port}_{self._config.entry_id}"
        if key is not None:
            if key == "dhcp":
                self._data = coordinator.data.get("hostname")[key]
            else:
                self._data = coordinator.data.get(key)[key]
            self._key = key
            self._attr_name = key
            self._attr_unique_id = f"{key}_{self._config.entry_id}"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        if self._port is not None:
            return BinarySensorDeviceClass.CONNECTIVITY
        return BinarySensorDeviceClass.RUNNING

    @property
    def entity_category(self):
        """Return the category of this binary_sensor."""
        if self._key is not None:
            return EntityCategory.DIAGNOSTIC
        return None  

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        if self._data is None:
            _LOGGER.warning("Data missing for: %s", self._attr_name)
            return False
        if self._port is not None:
            return self._data["Link Status Raw"]
        if self._key is not None:
            return self._data
        return False

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if self._port is not None and "stats" in self.coordinator.data.get("stats"):
            return True
        if self._key is not None and self._key in self.coordinator.data or self._key in self.coordinator.data.get("hostname"):
            return True
        return False

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if self._port is not None:
            return self._data
        return None
