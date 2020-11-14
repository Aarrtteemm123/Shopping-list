from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.icon_definitions import md_icons
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
        self.screen = Builder.load_file('app.kv')
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.button,
            items=[{"text": 'Settings'}, {"text": 'About project'}],
            width_mult=4
        )
        self.menu.bind(on_release=self.callback_menu_toolbar)

        self.dialog = MDDialog(
            title="Address:",
            type="custom",
            md_bg_color=[1, 1, 1, 1.0],
            content_cls=Content(),
            buttons=[
                MDFlatButton(
                    text="CANCEL", text_color=self.theme_cls.primary_color,on_release=self.dialog_close
                ),
                MDFlatButton(
                    text="OK", text_color=self.theme_cls.primary_color,on_release=self.click_ok
                ),
            ],
        )

        self.but_add = MDFloatingActionButton(
            icon="plus",
            pos_hint={"center_x": .9, "center_y": .1},
            md_bg_color=[0.11372549019607843, 0.9137254901960784, 0.7137254901960784, 1.0],
            on_release=self.dialog.open
        )
        self.screen.ids.screen_manager.get_screen('main').add_widget(self.but_add)
        for i in range(10):
            self.screen.ids.screen_manager.get_screen('main').ids.scroll_history.add_widget(
                TwoLineAvatarIconListItem(text=f"Item {i}", secondary_text = 'sec text', on_release=self.click_on_list_item)
            )
        for i in range(10):
            self.screen.ids.screen_manager.get_screen('main').ids.scroll_active.add_widget(
                TwoLineAvatarIconListItem(text=f"Item {i}", secondary_text = 'sec text', on_release=self.click_on_history_list_item)
            )

    def click_on_list_item(self,item):
        print(item.text)
        print(self.screen.ids.screen_manager.get_screen('main').ids.scroll_history.remove_widget(item))
        print(self.screen.ids.screen_manager.get_screen('main').ids.scroll_active.add_widget(item))

    def click_on_history_list_item(self,item):
        print(item.text)

    def click_ok(self,*args):
        print(self.dialog.content_cls.ids.item.text)
        print(self.dialog.content_cls.ids.number.text)
        print(self.dialog.content_cls.ids.details.text)
        self.dialog.dismiss()

    def dialog_close(self,*args):
        self.dialog.dismiss()

    def switch_color_mode(self, switch, value):
        if value:
            self.theme_cls.theme_style = 'Dark'
            self.dialog.md_bg_color = [0.15, 0.15, 0.15, 1.0]

        else:
            self.theme_cls.theme_style = 'Light'
            self.dialog.md_bg_color = [1, 1, 1, 1.0]

    def open_dialog(self):
        self.dialog.open()

    def change_screen(self, name_screen):
        self.root.ids.screen_manager.current = name_screen

    def callback_menu_toolbar(self, instance_menu, instance_menu_item):
        if instance_menu_item.text == 'Settings':
            self.change_screen('settings')
        if instance_menu_item.text == 'About project':
            self.change_screen('about')
        instance_menu.dismiss()

    def build(self):
        return self.screen


MyApp().run()
