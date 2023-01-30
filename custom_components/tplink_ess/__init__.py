"""
Custom integration to integrate TPLink Easy Smart Switches with Home Assistant.

For more details about this integration, please refer to
https://github.com/lyricnz/tplink_ess
"""
import asyncio
import logging
import random
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_MAC, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import TPLinkESSClient
from .const import DOMAIN, PLATFORMS, STARTUP_MESSAGE

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(
    hass: HomeAssistant, config: Config
):  # pylint: disable=unused-argument
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)
    switch_mac = entry.data.get(CONF_MAC)

    interval = timedelta(seconds=random.randint(10, 30))

    client = TPLinkESSClient(username, password, switch_mac)

    coordinator = TPLinkESSDataUpdateCoordinator(
        hass, client=client, name=switch_mac, interval=interval
    )
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True


class TPLinkESSDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: TPLinkESSClient,
        name: str,
        interval: int,
    ) -> None:
        """Initialize."""
        self.api = client
        self._interval = interval
        self.platforms = []

        super().__init__(hass, _LOGGER, name=name, update_interval=interval)

    async def _async_update_data(self):
        """Update data via library."""
        try:
            value = await self.api.async_get_data()
            _LOGGER.debug("TPLink switch data: %s", value)
        except Exception as exception:
            _LOGGER.debug("Error while refreshing switch data: %s", exception)
            raise UpdateFailed() from exception
        return value


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded
