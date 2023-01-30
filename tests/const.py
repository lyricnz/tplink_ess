"""Constants for tplink_ess tests."""

SWITCH_NAME = "test_switch"
CONFIG_DATA = {
    "mac": "70:4f:57:89:61:6a",
    "username": "admin",
    "password": "admin",
}

SWITCH_DATA = {
    "hostname": {
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
    "num_ports": {"num_ports": 5},
    "ports": {
        "ports": [
            "01:01:00:01:06:00:00",
            "02:01:00:01:00:00:00",
            "03:01:00:01:06:00:00",
            "04:01:00:01:00:00:00",
            "05:01:00:01:06:00:00",
        ]
    },
    "trunk": {"trunk": "01:00:00:00:00"},
    "mtu_vlan": {"mtu_vlan": "00:01"},
    "vlan": {
        "vlan_enabled": "01",
        "vlan": [
            {
                "VLAN ID": 1,
                "Member Ports": "1,2,3,4,5",
                "Tagged Ports": "",
                "VLAN Name": "Default_VLAN",
            },
            {
                "VLAN ID": 50,
                "Member Ports": "1,5",
                "Tagged Ports": "",
                "VLAN Name": "GAMING",
            },
        ],
        "vlan_filler": " ",
    },
    "pvid": {"pvid": [(1, 50), (2, 1), (3, 1), (4, 1), (5, 1)], "vlan_filler": " "},
    "qos1": {"qos1": True},
    "qos2": {"qos2": ["01:00", "02:00", "03:00", "04:00", "05:00"]},
    "mirror": {"mirror": "00:01:00:00:00:00:00:00:00:00"},
    "stats": {
        "stats": [
            {
                "Port": 1,
                "Status": "Enabled",
                "Status Raw": 1,
                "Link Status": "1000Full",
                "Link Status Raw": 6,
                "TxGoodPkt": 31560514,
                "TxBadPkt": 0,
                "RxGoodPkt": 1403717,
                "RxBadPkt": 0,
            },
            {
                "Port": 2,
                "Status": "Enabled",
                "Status Raw": 1,
                "Link Status": "Link Down",
                "Link Status Raw": 0,
                "TxGoodPkt": 0,
                "TxBadPkt": 0,
                "RxGoodPkt": 0,
                "RxBadPkt": 0,
            },
            {
                "Port": 3,
                "Status": "Enabled",
                "Status Raw": 1,
                "Link Status": "1000Full",
                "Link Status Raw": 6,
                "TxGoodPkt": 72797090,
                "TxBadPkt": 0,
                "RxGoodPkt": 27649623,
                "RxBadPkt": 0,
            },
            {
                "Port": 4,
                "Status": "Enabled",
                "Status Raw": 1,
                "Link Status": "Link Down",
                "Link Status Raw": 0,
                "TxGoodPkt": 0,
                "TxBadPkt": 0,
                "RxGoodPkt": 0,
                "RxBadPkt": 0,
            },
            {
                "Port": 5,
                "Status": "Enabled",
                "Status Raw": 1,
                "Link Status": "1000Full",
                "Link Status Raw": 6,
                "TxGoodPkt": 30053555,
                "TxBadPkt": 0,
                "RxGoodPkt": 73937797,
                "RxBadPkt": 25,
            },
        ]
    },
    "loop_prev": {"loop_prev": True},
}
