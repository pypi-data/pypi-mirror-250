from extras.plugins import PluginMenuItem, PluginMenu, PluginMenuButton
from utilities.choices import ButtonColorChoices
from django.conf import settings

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_counterparties', {})


class MyPluginMenu(PluginMenu):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = name

    @property
    def name(self):
        return self._name


if plugin_settings.get('enable_navigation_menu'):
    menuitem = []
    # Add a menu item for Counterparties if enabled
    if plugin_settings.get('enable_counterparties'):
        menuitem.append(
            PluginMenuItem(
                link='plugins:netbox_counterparties:counterparty_list',
                link_text='Контрагенты',
                buttons=[PluginMenuButton(
                    link='plugins:netbox_counterparties:counterparty_add',
                    title='Создать',
                    icon_class='mdi mdi-plus-thick',
                    color=ButtonColorChoices.GREEN
                )],
                permissions=['dcim.view_device']
            )
        )
        menuitem.append(
            PluginMenuItem(
                link='plugins:netbox_counterparties:counterpartygroup_list',
                link_text='Группы контрагентов',
                buttons=[PluginMenuButton(
                    link='plugins:netbox_counterparties:counterpartygroup_add',
                    title='Создать',
                    icon_class='mdi mdi-plus-thick',
                    color=ButtonColorChoices.GREEN
                )],
                permissions=['dcim.view_device']
            )
        )
        menuitem.append(
            PluginMenuItem(
                link='plugins:netbox_counterparties:counterpartyrole_list',
                link_text='Роли контрагентов',
                buttons=[PluginMenuButton(
                    link='plugins:netbox_counterparties:counterpartyrole_add',
                    title='Создать',
                    icon_class='mdi mdi-plus-thick',
                    color=ButtonColorChoices.GREEN
                )],
                permissions=['dcim.view_device']
            )
        )
        menuitem.append(
            PluginMenuItem(
                link='plugins:netbox_counterparties:counterpartyassignment_list',
                link_text='Привязка контрагентов',
                # buttons=[PluginMenuButton(
                #     link='plugins:netbox_counterparties:counterpartyassignment_add',
                #     title='Создать',
                #     icon_class='mdi mdi-plus-thick',
                #     color=ButtonColorChoices.GREEN
                # )],
                permissions=['dcim.view_device']
            )
        )

    # If we are using NB 3.4.0+ display the new top level navigation option
    if settings.VERSION >= '3.4.0':
        menu = MyPluginMenu(
            name='counterpartiesPl',
            label='Контрагенты',
            groups=(
                ('', menuitem),
            ),
            icon_class='mdi mdi-account-alert-outline'
        )

    else:
        # Fall back to pre 3.4 navigation option
        menu_items = menuitem
