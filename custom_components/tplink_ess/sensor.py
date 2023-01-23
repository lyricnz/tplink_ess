"""Sensor platform for tplink_ess."""
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, ICON
from .entity import TPLinkESSEntity

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    # Loop thru coordinator data keys
    sensors = []
    vlans = coordinator.data.get("vlan")["vlan"]
    i = 0
    for vlan in vlans:
        sensors.append(TPLinkESSSensor(i, "vlan", coordinator, entry))
        i = i + 1

    pvids = coordinator.data.get("pvid")["pvid"]
    i = 0
    for pvid in pvids:
        sensors.append(TPLinkESSSensor(i, "pvid", coordinator, entry))
        i = i + 1

    async_add_devices(sensors, False)


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
        self._config = config
        self._key = key
        self._prefix = coordinator.data.get("hostname")["hostname"]
        if key == "vlan" and "vlan" in coordinator.data:
            if "vlan" in coordinator.data.get("vlan"):
                self._data = coordinator.data.get("vlan")["vlan"][item_id]
                self._vlan_id = item_id
                self._vlan_id_num = self._data["VLAN ID"]
                self._attr_name = f"{self._prefix} VLAN: {self._data['VLAN Name']}"
                self._attr_unique_id = f"vlan{self._vlan_id_num}_{self._config.entry_id}"
        if key == "pvid":
            self._data = coordinator.data.get("pvid")["pvid"][item_id][1]
            self._pvid = item_id + 1
            self._attr_name = f"{self._prefix} PVID: {self._pvid}"
            self._attr_unique_id = f"pvid{self._pvid}_{self._config.entry_id}"

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        if self._key == "vlan":
            return self._data["VLAN ID"]
        if self._key == "pvid":
            return self._data
        return None

    @property
    def icon(self):
        """Return the icon of the sensor."""
        if self._key == "vlan":
            return "mdi:router-network"
        if self._key == "pvid":
            return "mdi:table-network"
        return ICON

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if self._key == "vlan":
            return self._data
        return None

    @property
    def entity_category(self):
        """Return the category of this binary_sensor."""
        if self._key == "vlan" or self._key == "pvid":
            return EntityCategory.CONFIG
        return None
