"""Sensor platform for tplink_ess."""
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN
from .entity import TPLinkESSEntity, TPLinkSensorEntityDescription

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_entities: AddEntitiesCallback):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    prefix = coordinator.data.get("hostname")["hostname"]

    # Loop thru coordinator data keys
    sensors = []
    if coordinator.data.get("vlan")["vlan_enabled"] == "01":
        vlans = coordinator.data.get("vlan")["vlan"]
        for i in range(len(vlans)):
            vlan_name = coordinator.data.get("vlan")["vlan"][i]["VLAN Name"]
            sensors.append(
                TPLinkESSSensor(
                    TPLinkSensorEntityDescription(
                        port=i,
                        name=f"{prefix} VLAN: {vlan_name}",
                        key="vlan",
                        entity_category=EntityCategory.CONFIG,
                        entity_registry_enabled_default=False,
                        icon="mdi:router-network",
                    ),
                    coordinator,
                    entry,
                ),
            )

    pvids = coordinator.data.get("pvid")["pvid"]
    for i in range(len(pvids)):
        sensors.append(
            TPLinkESSSensor(
                TPLinkSensorEntityDescription(
                    port=i,
                    name=f"{prefix} PVID: {i}",
                    key="pvid",
                    entity_category=EntityCategory.CONFIG,
                    entity_registry_enabled_default=False,
                    icon="mdi:table-network",
                ),
                coordinator,
                entry,
            ),
        )

    # Per Port sensors
    limit = coordinator.data.get("num_ports")["num_ports"]
    for i in range(limit):
        name = coordinator.data.get("stats")["stats"][i]["Port"]
        sensors.append(
            TPLinkESSSensor(
                TPLinkSensorEntityDescription(
                    port=i,
                    name=f"{prefix} Port {name} TxGoodPkt",
                    key="TxGoodPkt",
                    icon="mdi:upload-network",
                    unit_of_measurement="packets",
                    entity_registry_enabled_default=False,
                ),
                coordinator,
                entry,
            ),
        )
        sensors.append(
            TPLinkESSSensor(
                TPLinkSensorEntityDescription(
                    port=i,
                    name=f"{prefix} Port {name} RxGoodPkt",
                    key="RxGoodPkt",
                    icon="mdi:download-network",
                    unit_of_measurement="packets",
                    entity_registry_enabled_default=False,
                ),
                coordinator,
                entry,
            ),
        ),
        sensors.append(
            TPLinkESSSensor(
                TPLinkSensorEntityDescription(
                    port=i,
                    name=f"{prefix} Port {name} Link Status",
                    key="Link Status",
                    icon="mdi:ethernet-cable",
                    entity_registry_enabled_default=False,
                ),
                coordinator,
                entry,
            ),
        ),
        sensors.append(
            TPLinkESSSensor(
                TPLinkSensorEntityDescription(
                    port=i,
                    name=f"{prefix} Port {name} PPS RX",
                    key="RxGoodPkt",
                    icon="mdi:lan-pending",
                    unit_of_measurement="packets/s",
                    entity_registry_enabled_default=False,
                ),
                coordinator,
                entry,
            ),
        ),
        sensors.append(
            TPLinkESSSensor(
                TPLinkSensorEntityDescription(
                    port=i,
                    name=f"{prefix} Port {name} PPS TX",
                    key="TxGoodPkt",
                    icon="mdi:lan-pending",
                    unit_of_measurement="packets/s",
                    entity_registry_enabled_default=False,
                ),
                coordinator,
                entry,
            ),
        )
    async_add_entities(sensors, False)


class TPLinkESSSensor(TPLinkESSEntity, SensorEntity):
    """tplink_ess Sensor class."""

    def __init__(
        self,
        sensor_description: TPLinkSensorEntityDescription,
        coordinator: DataUpdateCoordinator,
        config: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, config)
        self.entity_description = sensor_description
        self.coordinator = coordinator
        self.data = coordinator.data
        self._item_id = sensor_description.port
        self._config = config
        self._key = sensor_description.key
        self._attr_name = sensor_description.name
        self._attr_unique_id = f"{sensor_description.name}_{config.entry_id}"
        self._attr_unit_of_measurement = sensor_description.unit_of_measurement
        self._last_reading = None

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        data = self.coordinator.data
        if self._key == "vlan":
            return data.get("vlan")["vlan"][self._item_id]["VLAN ID"]
        if self._key == "pvid":
            return data.get("pvid")["pvid"][self._item_id][1]
        if (
            value := data.get("stats")["stats"][self._item_id].get(self._key)
        ) is not None:
            if self._key in ("TxGoodPkt", "RxGoodPkt"):
                if self._attr_unit_of_measurement == "packets/s":
                    if self._last_reading is None:
                        self._last_reading = value
                    else:
                        self._last_reading = (
                            value - self._last_reading
                        ) / self.coordinator.update_interval
                    return float(self._last_reading)
                return int(value)
            if self._last_reading != value:
                self._last_reading = value
        return self._last_reading

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        data = self.coordinator.data
        if self._key == "vlan":
            return data.get("vlan")["vlan"][self._item_id]
        return None
