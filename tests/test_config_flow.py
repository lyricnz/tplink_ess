"""Test tplink_ess config flow."""

from unittest import mock
from unittest.mock import patch
import tplink_ess_lib
import pytest

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from custom_components.tplink_ess.const import DOMAIN

from tests.const import CONFIG_DATA

pytestmark = pytest.mark.asyncio

TEST_MAC = {"mac": "70:4f:57:89:61:6a"}
TEST_LOGIN = {
    "username": "admin",
    "password": "admin",
}
TEST_DISCOVERY_RESULTS = [
    {
        "type": "TL-SG105E",
        "hostname": "switch7",
        "mac": "70:4f:57:89:61:6a",
        "firmware": "1.0.0 Build 20160715 Rel.38605",
        "hardware": "TL-SG105E 3.0",
        "dhcp": False,
        "ip_addr": "192.168.1.109",
        "ip_mask": "255.255.255.0",
        "gateway": "192.168.1.4",
    },
]


async def _get_connection_form(
    hass: HomeAssistant, connection_type: str
) -> FlowResultType:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.MENU

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {"next_step_id": connection_type}
    )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}
    return result


async def test_discover(hass, mock_switch):
    """Test manual user entry."""
    with patch(
        "custom_components.tplink_ess.config_flow.TPLinkESSClient.async_discover_swithces",
        return_value=TEST_DISCOVERY_RESULTS,
    ):
        result = await _get_connection_form(hass, "discover")

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], TEST_MAC
        )
        assert result2["type"] == "form"
        assert result2["step_id"] == "creds"

        with patch(
            "custom_components.tplink_ess.config_flow.TPLinkESSFlowHandler._test_credentials",
            return_value=True,
        ), patch(
            "custom_components.tplink_ess.async_setup_entry", return_value=True
        ) as mock_setup_entry:

            result3 = await hass.config_entries.flow.async_configure(
                result["flow_id"], TEST_LOGIN
            )

            assert result3["type"] == "create_entry"
            assert result3["title"] == "switch7"
            assert result3["data"] == {
                "mac": "70:4f:57:89:61:6a",
                "password": "admin",
                "username": "admin",
            }

            await hass.async_block_till_done()
            assert len(mock_setup_entry.mock_calls) == 1


async def test_manual(hass, mock_switch):
    """Test manual user entry."""
    result = await _get_connection_form(hass, "manual")

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"], TEST_MAC
    )
    assert result2["type"] == "form"
    assert result2["step_id"] == "creds"

    with patch(
        "custom_components.tplink_ess.config_flow.TPLinkESSFlowHandler._test_credentials",
        return_value=True,
    ), patch(
        "custom_components.tplink_ess.async_setup_entry", return_value=True
    ) as mock_setup_entry:

        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"], TEST_LOGIN
        )

        assert result3["type"] == "create_entry"
        assert result3["title"] == "70:4f:57:89:61:6a"
        assert result3["data"] == {
            "mac": "70:4f:57:89:61:6a",
            "password": "admin",
            "username": "admin",
        }

        await hass.async_block_till_done()

        assert len(mock_setup_entry.mock_calls) == 1


async def test_manual_login_fail(hass):
    """Test manual user entry."""
    result = await _get_connection_form(hass, "manual")

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"], TEST_MAC
    )
    assert result2["type"] == "form"
    assert result2["step_id"] == "creds"

    result3 = await hass.config_entries.flow.async_configure(
        result["flow_id"], TEST_LOGIN
    )

    assert result3["errors"] == {"base": "auth"}
