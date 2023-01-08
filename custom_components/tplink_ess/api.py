"""Sample API Client."""

import logging
from tplink_ess_lib import MissingInterface, tplink_ess


_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class TPLinkESSClient:
    """Representation of a TPLink ESS network switch."""

    def __init__(
        self,
        username: str = "",
        password: str = "",
        mac_addr: str = "",
        interface: str = "",
    ) -> None:
        """Sample API Client."""
        self._username = username
        self._password = password
        self._mac_addr = mac_addr
        self._interface = interface

    async def async_get_data(self) -> dict:
        """Get data from the API."""
        api = tplink_ess(
            self._mac_addr, self._interface, self._username, self._password
        )
        return await api.update_data()

    async def async_get_interfaces(self) -> dict:
        """Get interface list from library."""
        api = tplink_ess()
        return await api.interfaces()

    async def async_discover_swithces(self) -> dict:
        """Discover switches and return results."""
        if not self._interface:
            raise MissingInterface
        api = tplink_ess(interface=self._interface)
        return await api.discovery()
