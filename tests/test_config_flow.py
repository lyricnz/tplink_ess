"""Test tplink_ess config flow."""
import itertools
from unittest.mock import patch

import pytest
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.tplink_ess import TPLinkESSClient
from custom_components.tplink_ess.const import DOMAIN

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
    {
        "auto_save": True,
        "dhcp": True,
        "firmware": "1.0.0 Build 20220706 Rel.55606",
        "gateway": "192.168.30.212",
        "hardware": "TL-SG105PE 2.0",
        "hostname": "Back-TL-SG105PE",
        "ip_addr": "192.168.30.50",
        "ip_mask": "255.255.255.0",
        "is_factory": False,
        "mac": "b4:b0:24:3a:f1:3b",
        "type": "TL-SG105PE",
    },
    {
        "dhcp": True,
        "firmware": "1.0.0 Build 20171214 Rel.70905",
        "gateway": "192.168.30.212",
        "hardware": "TL-SG108E 3.0",
        "hostname": "TL-SG108E",
        "ip_addr": "192.168.30.111",
        "ip_mask": "255.255.255.0",
        "mac": "b0:4e:26:45:ee:d8",
        "type": "TL-SG108E",
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
        "custom_components.tplink_ess.config_flow.TPLinkESSClient.async_discover_switches",
        return_value=TEST_DISCOVERY_RESULTS,
    ):
        result = await _get_connection_form(hass, "discover")

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], TEST_MAC
        )
        assert result2["type"] == "form"
        assert result2["step_id"] == "creds"

        with patch(
            "custom_components.tplink_ess.config_flow.TPLinkESSFlowHandler._validate_credentials",
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
        "custom_components.tplink_ess.config_flow.TPLinkESSFlowHandler._validate_credentials",
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


async def test_discovery_results(hass, mock_switch):
    """Test that the list of switches is returned in the same order however the results arrive."""
    found_switches = None
    for results in itertools.permutations(TEST_DISCOVERY_RESULTS):
        with patch("tplink_ess_lib.TpLinkESS.discovery", return_value=results):
            api = TPLinkESSClient()
            switches = await api.async_discover_switches()
            assert len(switches) == len(TEST_DISCOVERY_RESULTS)
            if found_switches is None:
                found_switches = switches
            assert switches == found_switches
