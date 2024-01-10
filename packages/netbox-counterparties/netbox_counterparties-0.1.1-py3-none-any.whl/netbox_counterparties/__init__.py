from extras.plugins import PluginConfig
# from dcim.models import Device
# from virtualization.models import VirtualMachine, Cluster
# from ipam.models import L2VPN, ASN, IPAddress, IPRange, Prefix, VLAN
# from extras.models import CustomField


class NetboxCounterparties(PluginConfig):
    name = 'netbox_counterparties'
    verbose_name = 'Контрагенты'
    description = 'Manage counterparties in Netbox'
    version = '0.0.1'
    author = 'Ilya Zakharov'
    author_email = 'me@izakharov.ru'
    min_version = '3.2.0'
    base_url = 'counterparties'
    default_settings = {
        "enable_navigation_menu": True,
        "enable_counterparties": True,
        "counterparties_location": "left",
    }


config = NetboxCounterparties


