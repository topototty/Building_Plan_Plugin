from netbox.plugins import PluginMenu, PluginMenuItem

menuitem1 = PluginMenuItem(
    link="plugins:netbox_plugin_buildingplan:building_plan_list",
    link_text="Building Plans",
)

menu = PluginMenu(
    label="Building Plans",
    groups=(
        ("Pages", (menuitem1,)),
    ),
    icon_class="mdi mdi-floor-plan",
)
