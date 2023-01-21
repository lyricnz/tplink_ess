"""Sample API Client."""

import logging

from tplink_ess_lib import tplink_ess

_LOGGER: logging.Logger = logging.getLogger(__package__)


class TPLinkESSClient:
    """Representation of a TPLink ESS network switch."""

    def __init__(
        self,
        username: str = "",
        password: str = "",
        switch_mac: str = "",
    ) -> None:
        """Library client."""
        self._username = username
        self._password = password
        self._switch_mac = switch_mac
        self._host_mac = "de:ad:be:ef:fe:ed"

    async def async_get_data(self) -> dict:
        """Get data from the API."""
        api = tplink_ess(self._host_mac, self._username, self._password)
        return await api.update_data(switch_mac=self._switch_mac)

    async def async_discover_swithces(self) -> list:
        """Discover switches and return results."""
        api = tplink_ess()
        return await api.discovery()
