# TP-Link Easy Smart Switch Integration for Home Assistant

This component queries local TP-Link ESS (Easy Smart Switches) to obtain
system information, port status and statistics, VLAN configuration, etc.

# tplink_ess

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

**This component will set up the following platforms.**

Platform | Description
-- | --
`binary_sensor` | Show port connected/disconnected status.
`sensor` | Show info from your TPLink Easy Smart Switch.

![example][exampleimg]

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `tplink_ess`.
4. Download _all_ the files from the `custom_components/tplink_ess/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "TPLink ESS"
8. Select either manual configuration (by MAC address) or automatic discovery (by broadcast) and select one
9. Enter the admin username+password for your switch
10. Select the Area for the device and click Finish

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[tplink_ess]: https://github.com/lyricnz/tplink_ess
[commits-shield]: https://img.shields.io/github/commit-activity/y/lyricnz/tplink_ess.svg?style=for-the-badge
[commits]: https://github.com/lyricnz/tplink_ess/commits/master
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/lyricnz/tplink_ess.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Simon%20Roberts%20%40lyricnz-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/lyricnz/tplink_ess.svg?style=for-the-badge
[releases]: https://github.com/lyricnz/tplink_ess/releases
