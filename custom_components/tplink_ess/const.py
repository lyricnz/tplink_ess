"""Constants for tplink_ess."""
# Base component constants
NAME = "TPLink ESS"
DOMAIN = "tplink_ess"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.0"
ISSUE_URL = "https://github.com/lyricnz/tplink_ess/issues"
MANUFACTURER = "TPLink"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
SWITCH = "switch"
PLATFORMS = [BINARY_SENSOR, SENSOR]

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
