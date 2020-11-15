from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.tab import MDTabsBase


class MainScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class AboutScreen(Screen):
    pass


class Tab(FloatLayout, MDTabsBase):
    pass


class Content(BoxLayout):
    pass


class MyApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = JsonStore('data.json')
        self.buffer_item = None
        self.auto_clear = False
        self.screen = Builder.load_file('app.kv')
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.button,
            items=[{"text": 'Settings'}, {"text": 'About project'}],
            width_mult=4
        )
        self.menu.bind(on_release=self.callback_menu_toolbar)

        self.dialog_new_item = MDDialog(
            title="Address:",
            type="custom",
            md_bg_color=[1, 1, 1, 1.0],
            content_cls=Content(),
            buttons=[
                MDFlatButton(
                    text="CANCEL", text_color=self.theme_cls.primary_color, on_release=self.dialog_new_item_close
                ),
                MDFlatButton(
                    text="OK", text_color=self.theme_cls.primary_color, on_release=self.dialog_new_item_ok
                ),
            ],
        )

        self.dialog_complete = MDDialog(
            title="Complete item",
            text="Do you want the item to move into the history?\n(If auto clear enable, item will be deleted)",
            md_bg_color=[1, 1, 1, 1.0],
            buttons=[
                MDFlatButton(
                    text="NO", text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_complete_no
                ),
                MDFlatButton(
                    text="YES", text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_complete_yes
                ),
            ],
        )

        self.dialog_delete = MDDialog(
            title="Delete item",
            text="Are you sure you want to delete this item?\nYou will not restore them after delete",
            md_bg_color=[1, 1, 1, 1.0],
            buttons=[
                MDFlatButton(
                    text="NO", text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_delete_no
                ),
                MDFlatButton(
                    text="YES", text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_delete_yes
                ),
            ],
        )

        self.but_add = MDFloatingActionButton(
            icon="plus",
            pos_hint={"center_x": .9, "center_y": .1},
            md_bg_color=[0.11372549019607843, 0.9137254901960784, 0.7137254901960784, 1.0],
            on_release=self.click_but_add
        )
        self.screen.ids.screen_manager.get_screen('main').add_widget(self.but_add)
        for i in range(10):
            self.screen.ids.screen_manager.get_screen('main').ids.scroll_history.add_widget(
                TwoLineAvatarIconListItem(text=f"Item {i}", secondary_text='history text',
                                          on_release=self.click_on_history_list_item)
            )
        for i in range(10):
            self.screen.ids.screen_manager.get_screen('main').ids.scroll_active.add_widget(
                TwoLineAvatarIconListItem(text=f"Item {i}", secondary_text='active text',
                                          on_release=self.click_on_active_list_item)
            )

    def click_but_add(self, *args):
        self.dialog_new_item.content_cls.ids.item.text = ''
        self.dialog_new_item.content_cls.ids.number.text = ''
        self.dialog_new_item.content_cls.ids.details.text = ''
        self.dialog_new_item.open()

    def dialog_complete_yes(self, *args):
        self.dialog_complete.dismiss()
        self.screen.ids.screen_manager.get_screen('main').ids.scroll_active.remove_widget(self.buffer_item)
        if not self.auto_clear:
            self.buffer_item = TwoLineAvatarIconListItem(text=self.buffer_item.text,
                                                         secondary_text=self.buffer_item.secondary_text,
                                                         on_release=self.click_on_history_list_item)
            self.screen.ids.screen_manager.get_screen('main').ids.scroll_history.add_widget(self.buffer_item)
        self.buffer_item = None

    def dialog_complete_no(self, *args):
        self.dialog_complete.dismiss()
        self.buffer_item = None

    def dialog_delete_no(self, *args):
        self.dialog_delete.dismiss()
        self.buffer_item = None

    def dialog_delete_yes(self, *args):
        self.dialog_delete.dismiss()
        self.screen.ids.screen_manager.get_screen('main').ids.scroll_history.remove_widget(self.buffer_item)
        self.buffer_item = None

    def click_on_active_list_item(self, item):
        self.buffer_item = item
        self.dialog_complete.open()

    def click_on_history_list_item(self, item):
        self.buffer_item = item
        self.dialog_delete.open()

    def dialog_new_item_ok(self, *args):
        item = self.dialog_new_item.content_cls.ids.item.text
        number = self.dialog_new_item.content_cls.ids.number.text
        details = self.dialog_new_item.content_cls.ids.details.text
        self.screen.ids.screen_manager.get_screen('main').ids.scroll_active.add_widget(
            TwoLineAvatarIconListItem(text=item + '  ' + number, secondary_text=details,
                                      on_release=self.click_on_active_list_item))
        self.dialog_new_item.dismiss()

    def dialog_new_item_close(self, *args):
        self.dialog_new_item.dismiss()

    def switch_clear_mode(self, switch, value):
        self.auto_clear = value

    def switch_color_mode(self, switch, value):
        if value:
            self.theme_cls.theme_style = 'Dark'
            self.dialog_new_item.md_bg_color = [0.15, 0.15, 0.15, 1.0]
            self.dialog_complete.md_bg_color = [0.15, 0.15, 0.15, 1.0]
            self.dialog_delete.md_bg_color = [0.15, 0.15, 0.15, 1.0]
        else:
            self.theme_cls.theme_style = 'Light'
            self.dialog_new_item.md_bg_color = [1, 1, 1, 1.0]
            self.dialog_complete.md_bg_color = [1, 1, 1, 1.0]
            self.dialog_delete.md_bg_color = [1, 1, 1, 1.0]

    def change_screen(self, name_screen):
        self.root.ids.screen_manager.current = name_screen

    def callback_menu_toolbar(self, instance_menu, instance_menu_item):
        if instance_menu_item.text == 'Settings':
            self.change_screen('settings')
        if instance_menu_item.text == 'About project':
            self.change_screen('about')
        instance_menu.dismiss()

    def on_stop(self):
        self.store.put('settings',
                       auto_clear = self.auto_clear,
                       color_mode = self.theme_cls.theme_style,
                       switch_color_mode_value=self.screen.ids.screen_manager.get_screen('settings').ids.color_mode.active,
                       switch_clear_mode_value=self.screen.ids.screen_manager.get_screen('settings').ids.clear_mode.active)

    def on_start(self):
        settings = self.store.get('settings')
        self.auto_clear = settings['auto_clear']
        self.theme_cls.theme_style = settings['color_mode']
        self.screen.ids.screen_manager.get_screen('settings').ids.color_mode.active = settings['switch_color_mode_value']
        self.screen.ids.screen_manager.get_screen('settings').ids.clear_mode.active = settings['switch_clear_mode_value']

    def build(self):
        return self.screen


MyApp().run()
