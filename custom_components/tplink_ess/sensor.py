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

    @property
    def native_unit_of_measurement(self) -> Any:
        """Return the unit of measurement."""
        if self._key in ("TxGoodPkt", "RxGoodPkt"):
            return "packets"
        return None

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        data = self.coordinator.data
        if self._key == "vlan":
            return data.get("vlan")["vlan"][self._item_id]["VLAN ID"]
        if self._key == "pvid":
            return data.get("pvid")["pvid"][self._item_id][1]
        if self._key in data.get("stats")["stats"][self._item_id]:
            if self._key in ("TxGoodPkt", "RxGoodPkt"):
                return int(data.get("stats")["stats"][self._item_id][self._key])
            return data.get("stats")["stats"][self._item_id][self._key]
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        data = self.coordinator.data
        if self._key == "vlan":
            return data.get("vlan")["vlan"][self._item_id]
        return None
