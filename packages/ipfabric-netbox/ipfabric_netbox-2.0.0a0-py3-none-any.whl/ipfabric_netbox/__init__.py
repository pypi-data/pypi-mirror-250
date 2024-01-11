from django.db import connection
from extras.plugins import PluginConfig


class NetboxIPFabricConfig(PluginConfig):
    name = "ipfabric_netbox"
    verbose_name = "NetBox IP Fabric SoT Plugin"
    description = "Sync IP Fabric into NetBox"
    version = "2.0.0a0"
    base_url = "ipfabric"

    def ready(self):
        super().ready()
        try:
            from ipfabric_netbox.signals import ipfabric_netbox_init

            all_tables = connection.introspection.table_names()
            if "extras_customfield" in all_tables:
                ipfabric_netbox_init()
        except Exception as e:
            print(f"Failed to initialize IP Fabric plugin: {e}.")


config = NetboxIPFabricConfig
