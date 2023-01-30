"""Binary sensor platform for tplink_ess."""
import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN
from .entity import TPLinkBinarySensorEntityDescription, TPLinkESSEntity

_LOGGER: logging.Logger = logging.getLogger(__package__)

BINARY_SENSORS_TYPES: tuple[TPLinkBinarySensorEntityDescription, ...] = (
    TPLinkBinarySensorEntityDescription(
        name="QoS",
        key="qos1",
        device_class=BinarySensorDeviceClass.RUNNING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    TPLinkBinarySensorEntityDescription(
        name="Loop Prevention",
        key="loop_prev",
        device_class=BinarySensorDeviceClass.RUNNING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    TPLinkBinarySensorEntityDescription(
        name="DHCP",
        key="dhcp",
        device_class=BinarySensorDeviceClass.RUNNING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


async def async_setup_entry(hass, entry, async_add_entities: AddEntitiesCallback):
    """Setup binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    binary_sensors = []
    limit = coordinator.data.get("num_ports")["num_ports"]
    prefix = coordinator.data.get("hostname")["hostname"]

    for i in range(limit):
        binary_sensors.append(
            TPLinkESSBinarySensor(
                TPLinkBinarySensorEntityDescription(
                    port=i,
                    key=None,
                    name=f"{prefix} Port {i+1}",
                    device_class=BinarySensorDeviceClass.CONNECTIVITY,
                ),
                coordinator,
                entry,
            )
        )

    for binary_sensor in BINARY_SENSORS_TYPES:
        binary_sensors.append(TPLinkESSBinarySensor(binary_sensor, coordinator, entry))

    async_add_entities(binary_sensors, False)


class TPLinkESSBinarySensor(TPLinkESSEntity, BinarySensorEntity):
    """TPLink ESS binary_sensor class."""

    def __init__(
        self,
        sensor_description: TPLinkBinarySensorEntityDescription,
        coordinator: DataUpdateCoordinator,
        config: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, config)
        self.entity_description = sensor_description
        self.coordinator = coordinator
        self._config = config
        self._port = sensor_description.port
        self._key = sensor_description.key
        self._prefix = coordinator.data.get("hostname")["hostname"]
        self._attr_name = sensor_description.name

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
