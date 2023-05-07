"""Sample API Client."""

import logging

from tplink_ess_lib import TpLinkESS

_LOGGER: logging.Logger = logging.getLogger(__package__)


class TPLinkESSClient:
    """Representation of a TPLink ESS network switch."""
    ACTION_NAMES = {'hostname', 'vlan', 'pvid', 'num_ports', 'stats'}

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
        api = TpLinkESS(self._host_mac, self._username, self._password)
        return await api.update_data(
            switch_mac=self._switch_mac,
            action_names=TPLinkESSClient.ACTION_NAMES)

    async def async_discover_switches(self) -> list:
        """Discover switches and return results."""
        api = TpLinkESS(self._host_mac)
        switches = await api.discovery()
        return sorted(switches, key=lambda k: k["hostname"] + k["mac"])
