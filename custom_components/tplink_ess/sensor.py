"""Sensor platform for tplink_ess."""
from homeassistant.components.sensor import SensorEntity

from .const import DEFAULT_NAME, DOMAIN, ICON, SENSOR
from .entity import TPLinkESSEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    # Loop thru coordinator data keys
    async_add_devices([TPLinkESSSensor(coordinator, entry)])


class TPLinkESSSensor(TPLinkESSEntity, SensorEntity):
    """integration_blueprint Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{SENSOR}"

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return self.coordinator.data.get("body")

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON
