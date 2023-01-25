"""Binary sensor platform for integration_blueprint."""
import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import BINARY_SENSOR_DEVICE_CLASS, DOMAIN, MANUFACTURER
from .entity import TPLinkESSEntity

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_entities: AddEntitiesCallback):
    """Setup binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    binary_sensors = []
    limit = coordinator.data.get("num_ports")["num_ports"]

    binary_sensors.extend(
        TPLinkESSBinarySensor(i, None, coordinator, entry) for i in range(limit)
    )

    # one off binary sensors
    binary_sensors.append(TPLinkESSBinarySensor(None, "qos1", coordinator, entry))
    binary_sensors.append(TPLinkESSBinarySensor(None, "loop_prev", coordinator, entry))
    binary_sensors.append(TPLinkESSBinarySensor(None, "dhcp", coordinator, entry))

    async_add_entities(binary_sensors, False)


class TPLinkESSBinarySensor(TPLinkESSEntity, BinarySensorEntity):
    """TPLink ESS binary_sensor class."""

    def __init__(
        self,
        port: int | None,
        key: str | None,
        coordinator: DataUpdateCoordinator,
        config: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, config)
        self.coordinator = coordinator
        self._config = config
        self._port = port
        self._key = key
        self._prefix = coordinator.data.get("hostname")["hostname"]

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        if self._port is not None:
            data = self.coordinator.data.get("stats")["stats"][self._port]
            return f"{self._prefix} Port {data['Port']}"
        if self._key is not None:
            if self._key == "dhcp":
                data = self.coordinator.data.get("hostname")[self._key]
            else:
                data = self.coordinator.data.get(self._key)[self._key]
            return f"{self._prefix} {self._key}"

    @property
    def unique_id(self):
        """
        Return a unique, Home Assistant friendly identifier for this entity.
        """
        if self._port is not None:
            return f"port{self._port}_{self._config.entry_id}"
        if self._key is not None:
            return f"{self._key}_{self._config.entry_id}"


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
        data = self.coordinator.data
        if data is None:
            _LOGGER.warning("Data missing for: %s", self._attr_name)
            return False
        if self._port is not None:
            return data.get("stats")["stats"][self._port]["Link Status Raw"]
        if self._key is not None:
            if self._key == "dhcp":
                return data.get("hostname")[self._key]
            return data.get(self._key)[self._key]
        return False

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if self._port is not None and "stats" in self.coordinator.data.get("stats"):
            return True
        if (
            self._key is not None
            and self._key in self.coordinator.data
            or self._key in self.coordinator.data.get("hostname")
        ):
            return True
        return False

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        data = self.coordinator.data
        if self._port is not None:
            return data.get("stats")["stats"][self._port]
        return None
