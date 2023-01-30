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


@pytest.fixture(autouse=True, name="mock_setup_entry")
async def fixture_mock_setup():
    """Make sure we never actually run setup."""
    with patch(
        "custom_components.tplink_ess.async_setup_entry", return_value=True
    ) as mock_setup_entry:
        yield


@pytest.fixture()
async def mock_test_creds():
    """Mock TPLinkESSClient for _test_credentials function."""
    with patch(
        "custom_components.tplink_ess.api.TPLinkESSClient",
    ) as mock_test_creds:
        # mock_lib = mock.Mock(spec=tplink_ess_lib)
        # mock_test_creds.return_value = mock_lib
        mock_test_creds.async_get_data.return_value = True
        yield mock_test_creds


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


async def test_manual(hass, mock_setup_entry, mock_test_creds):
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

    assert result3["errors"] == {}

    assert result3["type"] == "create_entry"
    assert result3["title"] == "70:4f:57:89:61:6a"
    assert result3["data"] == ""

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

    assert result3["errors"] == {'base': 'auth'}
