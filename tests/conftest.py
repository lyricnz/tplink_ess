"""Global fixtures for integration_blueprint integration."""

from unittest.mock import patch

import pytest

from tests.const import SWITCH_DATA

pytest_plugins = "pytest_homeassistant_custom_component"


# This fixture enables loading custom integrations in all tests.
# Remove to enable selective use of this fixture
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    yield


# This fixture is used to prevent HomeAssistant from attempting to create and dismiss persistent
# notifications. These calls would fail without this fixture since the persistent_notification
# integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture():
    """Skip notification calls."""
    with patch("homeassistant.components.persistent_notification.async_create"), patch(
        "homeassistant.components.persistent_notification.async_dismiss"
    ):
        yield


@pytest.fixture()
def mock_switch():
    """Mock switch data."""
    with patch(
        "custom_components.tplink_ess.TPLinkESSDataUpdateCoordinator._async_update_data"
    ) as mock_value:
        mock_value.return_value = SWITCH_DATA
        yield mock_value

