from netbox.choices import ButtonColorChoices  
from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton

# Создаем список кнопок для элемента меню, здесь одна кнопка для добавления нового плана здания.
building_plan_buttons = [
    PluginMenuButton(
        link="plugins:netbox_plugin_buildingplan:buildingplan_add",  # URL-адрес для перехода при нажатии на кнопку.
        title='Add',  # Текст, который будет отображаться при наведении на кнопку.
        icon_class='mdi mdi-plus-thick',  # CSS-класс для иконки на кнопке (используется Material Design Icons).
        color=ButtonColorChoices.GREEN  # Цвет кнопки, используется зеленый цвет.
    )
]

# Создаем элемент меню для отображения списка планов зданий.
menuitem1 = PluginMenuItem(
    link="plugins:netbox_plugin_buildingplan:buildingplan_list",  # URL-адрес для перехода при выборе этого элемента меню.
    link_text="Building Plans",  # Текст, который будет отображаться в меню.
    buttons=building_plan_buttons  # Кнопки, которые будут отображаться рядом с элементом меню.
)

# Создаем само меню плагина, которое будет отображаться в интерфейсе NetBox.
menu = PluginMenu(
    label="Building Plans",  # Метка для меню, которая будет отображаться в интерфейсе.
    groups=(
        ("Building Plans", (menuitem1,)),  # Группа элементов меню; в данном случае только один элемент.
    ),
    icon_class="mdi mdi-floor-plan",  # CSS-класс для иконки меню (используется Material Design Icons).
)
