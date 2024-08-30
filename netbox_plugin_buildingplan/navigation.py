from netbox.choices import ButtonColorChoices
from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton


building_plan_buttons = [
    PluginMenuButton(
        link="plugins:netbox_plugin_buildingplan:buildingplan_add",
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN)
]

menuitem1 = PluginMenuItem(
    link="plugins:netbox_plugin_buildingplan:buildingplan_list",
    link_text="Building Plans",
    buttons=building_plan_buttons
)


menu = PluginMenu(
    label="Building Plans",
    groups=(
        ("Building Plans", (menuitem1,)),
    ),
    icon_class="mdi mdi-floor-plan",
)
