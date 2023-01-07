"""Adds config flow for tplink_ess."""
from homeassistant import config_entries
from homeassistant.const import CONF_MAC, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import callback
import voluptuous as vol

from .api import TPLinkESSClient
from .const import (
    CONF_INTERFACE,
    DOMAIN,
    PLATFORMS,
)


class TPLinkESSFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Blueprint."""

    VERSION = 1

    def __init__(self):
        """Initialize."""
        self._errors = {}
        self._data = {}

    async def async_step_user(self, user_input=None): # pylint: disable=unused-argument
        """Handle a flow initialized by the user."""
        self._errors = {}

        return self.async_show_menu(step_id="user", menu_options=["manual", "discover"])

    async def async_step_discover(self, user_input=None):
        """Handle switch discovery."""
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_mac()
        else:
            return await self._show_config_discovery(user_input)

    async def _show_config_discovery(self, user_input):
        """Show the configuration form."""
        api = TPLinkESSClient()
        interfaces = await api.async_get_interfaces()

        return self.async_show_form(
            step_id="discover",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_INTERFACE, default=user_input[CONF_INTERFACE]
                    ): vol.In(interfaces),
                }
            ),
            errors=self._errors,
        )

    async def async_step_mac(self, user_input=None):
        """Handle MAC address selection."""
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_creds()
        else:
            return await self._show_config_mac(user_input)

    async def _show_config_mac(self, user_input):
        """Show the configuration form."""
        api = TPLinkESSClient(interface=self._data[CONF_INTERFACE])
        switches = await api.async_discover_swithces()
        sw_list = []

        for switch in switches:
            sw_list.append(switch[CONF_MAC])

        return self.async_show_form(
            step_id="discover",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_MAC, default=user_input[CONF_MAC]): vol.In(
                        sw_list
                    ),
                }
            ),
            errors=self._errors,
        )

    async def async_step_manual(self, user_input=None):
        """Handle manual user input for switch."""
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_creds()
        else:
            return await self._show_config_manual(user_input)

    async def _show_config_manual(self, user_input):
        """Show the config form."""
        api = TPLinkESSClient()
        interfaces = api.async_get_interfaces()

        return self.async_show_form(
            step_id="discover",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_INTERFACE, default=user_input[CONF_INTERFACE]
                    ): vol.In(interfaces),
                    vol.Required(CONF_MAC, default=user_input[CONF_MAC]): str,
                }
            ),
            errors=self._errors,
        )

    async def async_step_creds(self, user_input=None):
        """Handle credential inputs from user."""
        if user_input is not None:
            valid = await self._test_credentials(
                user_input[CONF_USERNAME],
                user_input[CONF_PASSWORD],
                user_input[CONF_MAC],
                user_input[CONF_INTERFACE],
            )
            if valid:
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME], data=user_input
                )
            else:
                self._errors["base"] = "auth"

            return await self._show_config_form(user_input)

        user_input = {}
        # Provide defaults for form
        user_input[CONF_USERNAME] = ""
        user_input[CONF_PASSWORD] = ""

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Handle options flow."""
        return TPLinkESSOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME, default=user_input[CONF_USERNAME]): str,
                    vol.Required(CONF_PASSWORD, default=user_input[CONF_PASSWORD]): str,
                }
            ),
            errors=self._errors,
        )

    async def _test_credentials(self, username, password, mac_addr, interface):
        """Return true if credentials is valid."""
        try:
            client = TPLinkESSClient(username, password, mac_addr, interface)
            await client.async_get_data()
            return True
        except Exception:  # pylint: disable=broad-except
            pass
        return False


class TPLinkESSOptionsFlowHandler(config_entries.OptionsFlow):
    """Blueprint config flow options handler."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_USERNAME), data=self.options
        )
