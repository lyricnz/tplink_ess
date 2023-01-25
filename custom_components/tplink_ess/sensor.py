"""Sensor platform for tplink_ess."""
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, ICON
from .entity import TPLinkESSEntity

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_entities: AddEntitiesCallback):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    # Loop thru coordinator data keys
    sensors = []
    if coordinator.data.get("vlan")["vlan_enabled"] == "01":
        vlans = coordinator.data.get("vlan")["vlan"]
        sensors.extend(
            TPLinkESSSensor(i, "vlan", coordinator, entry) for i in range(len(vlans))
        )

    pvids = coordinator.data.get("pvid")["pvid"]
    sensors.extend(
        TPLinkESSSensor(i, "pvid", coordinator, entry) for i in range(len(pvids))
    )

    # Port packet counters
    limit = coordinator.data.get("num_ports")["num_ports"]
    sensors.extend(
        TPLinkESSSensor(i, "TxGoodPkt", coordinator, entry) for i in range(limit)
    )
    sensors.extend(
        TPLinkESSSensor(i, "RxGoodPkt", coordinator, entry) for i in range(limit)
    )

    async_add_entities(sensors, False)


class TPLinkESSSensor(TPLinkESSEntity, SensorEntity):
    """integration_blueprint Sensor class."""

    def __init__(
        self,
        item_id: int | None,
        key: str | None,
        coordinator: DataUpdateCoordinator,
        config: ConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, config)
        self.coordinator = coordinator
        self.data = coordinator.data
        self._config = config
        self._key = key
        self._prefix = self.data.get("hostname")["hostname"]
        self._item_id = item_id


    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        data = self.coordinator.data
        if self._key == "vlan":
            vlan_name = data.get("vlan")["vlan"][self._item_id]["VLAN Name"]
            return f"{self._prefix} VLAN: {vlan_name}"
        if self._key == "pvid":
            pvid = self._item_id + 1
            return f"{self._prefix} PVID: {pvid}"
        if self._key in ("TxGoodPkt", "RxGoodPkt"):
            name = data.get("stats")["stats"][self._item_id]["Port"]
            return f"{self._prefix} Port {name} {self._key}"


    @property
    def unique_id(self):
        """
        Return a unique, Home Assistant friendly identifier for this entity.
        """
        data = self.coordinator.data
        if self._key == "vlan":
            vlan_id_num = data.get("vlan")["vlan"][self._item_id]["VLAN ID"]
            return f"vlan{vlan_id_num}_{self._config.entry_id}"  
        if self._key == "pvid":
            pvid = self._item_id + 1
            return f"pvid{pvid}_{self._config.entry_id}"  
        if self._key in ("TxGoodPkt", "RxGoodPkt"):
            return f"port{self._item_id}_{self._key}_{self._config.entry_id}"

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
        if self._key in ("TxGoodPkt", "RxGoodPkt"):
            return int(data.get("stats")["stats"][self._item_id][self._key])
        return None

    @property
    def icon(self):
        """Return the icon of the sensor."""
        if self._key == "vlan":
            return "mdi:router-network"
        if self._key == "pvid":
            return "mdi:table-network"
        if self._key == "TxGoodPkt":
            return "mdi:upload-network"
        if self._key == "RxGoodPkt":
            return "mdi:download-network"
        return ICON

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        data = self.coordinator.data
        if self._key == "vlan":
            return data.get("vlan")["vlan"][self._item_id]
        return None

    @property
    def entity_category(self):
        """Return the category of this binary_sensor."""
        if self._key in ("vlan", "pvid"):
            return EntityCategory.CONFIG
        return None

    @property
    def entity_registry_enabled_default(self):
        """Return the default enablment of a sensor."""
        # Disable sensors by default
        return False
