"""Test tplink_ess config flow."""
from unittest.mock import patch

import pytest

from custom_components.tplink_ess import TPLinkESSClient

pytestmark = pytest.mark.asyncio

TEST_DISCOVERY_RESULTS = [
    {
        "type": "TL-SG105E",
        "hostname": "switch7",
        "mac": "70:4f:57:89:61:6a",
    },
    {
        "type": "TL-SG105PE",
        "hostname": "Back-TL-SG105PE",
        "mac": "b4:b0:24:3a:f1:3b",
    },
    {
        "type": "TL-SG108E",
        "hostname": "TL-SG108E",
        "mac": "b0:4e:26:45:ee:d8",
    },
]


async def test_discovery_results(hass, mock_switch):
    """Test that the list of switches is sorted."""
    with patch(
        "tplink_ess_lib.TpLinkESS.discovery",
        return_value=TEST_DISCOVERY_RESULTS,
    ):
        api = TPLinkESSClient()
        switches = await api.async_discover_switches()
        assert len(switches) == 3
        names = [switch["hostname"] for switch in switches]
        assert names == sorted(names)
