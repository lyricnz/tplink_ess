"""Adds config flow for tplink_ess."""
import logging

from homeassistant import config_entries
from homeassistant.const import CONF_MAC, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import callback
from homeassistant.helpers.device_registry import format_mac
import voluptuous as vol

from .api import TPLinkESSClient
from .const import DOMAIN, PLATFORMS

_LOGGER: logging.Logger = logging.getLogger(__package__)


class TPLinkESSFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Blueprint."""

    VERSION = 1

    def __init__(self):
        """Initialize."""
        self._errors = {}
        self._data = {}
        self._switches = {}

    async def async_step_user(self, user_input=None):  # pylint: disable=unused-argument
        """Handle a flow initialized by the user."""
        self._errors = {}

        return self.async_show_menu(step_id="user", menu_options=["manual", "discover"])

    async def async_step_discover(self, user_input=None):
        """Handle switch discovery."""
        if user_input is not None:
            unique_id = format_mac(user_input[CONF_MAC])
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured(
                updates={
                    CONF_MAC: user_input[CONF_MAC]
                },
            )            
            self._data.update(user_input)
            return await self.async_step_creds()
        return await self._show_config_discovery(user_input)

    async def _show_config_discovery(self, user_input):
        """Show the configuration form."""
        api = TPLinkESSClient()
        switches = await api.async_discover_swithces()

        _LOGGER.debug("Discover results: %s", switches)

        if len(switches) == 0:
            _LOGGER.error("No switches discovered.")
            discovered = {"": "None found"}

        else:
            discovered = {}
            for switch in switches:
                discovered[
                    switch["mac"]
                ] = f"{switch['ip_addr']} ({switch['hostname']} - {switch['hardware']})"
                self._switches[switch["mac"]] = switch['hostname']

        _LOGGER.debug("Discovered processed: %s", discovered)

        if user_input is None:
            return self.async_show_form(
                step_id="discover",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_MAC): vol.In(discovered),
                    }
                ),
                errors=self._errors,
            )

        return self.async_show_form(
            step_id="discover",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_MAC, default=user_input[CONF_MAC]): vol.In(
                        discovered
                    ),
                }
            ),
            errors=self._errors,
        )

    async def async_step_manual(self, user_input=None):
        """Handle manual user input for switch."""
        if user_input is not None:
            unique_id = format_mac(user_input[CONF_MAC])
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured(
                updates={
                    CONF_MAC: user_input[CONF_MAC]
                },
            )
            self._data.update(user_input)
            return await self.async_step_creds()
        return await self._show_config_manual(user_input)

    async def _show_config_manual(self, user_input):
        """Show the config form."""

        if user_input is None:
            return self.async_show_form(
                step_id="manual",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_MAC): str,
                    }
                ),
                errors=self._errors,
            )
        return self.async_show_form(
            step_id="manual",
            data_schema=vol.Schema(
                {
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
                self._data[CONF_MAC],
            )
            if valid:
                self._data.update(user_input)
                return self.async_create_entry(
                    title=self._switches[self._data[CONF_MAC]], data=self._data
                )
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
        if user_input is None:
            return self.async_show_form(
                step_id="creds",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_USERNAME): str,
                        vol.Required(CONF_PASSWORD): str,
                    }
                ),
                errors=self._errors,
            )
        return self.async_show_form(
            step_id="creds",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME, default=user_input[CONF_USERNAME]): str,
                    vol.Required(CONF_PASSWORD, default=user_input[CONF_PASSWORD]): str,
                }
            ),
            errors=self._errors,
        )

    async def _test_credentials(self, username, password, mac_addr):
        """Return true if credentials is valid."""
        try:
            client = TPLinkESSClient(username, password, mac_addr)
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
