from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.picker import MDDatePicker
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
            # caller=self.screen.ids.screen_manager.get_screen('main').ids.button,
            items=[{"text": 'Settings'}, {"text": 'About project'}],
            width_mult=4
        )
        self.menu.bind(on_release=self.callback)
        self.rebuild_dialog()

    def rebuild_dialog(self):
        self.dialog = MDDialog(
            title="Address:",
            type="custom",
            content_cls=Content(),
            buttons=[
                MDFlatButton(
                    text="CANCEL", text_color=self.theme_cls.primary_color,
                ),
                MDFlatButton(
                    text="OK", text_color=self.theme_cls.primary_color,
                ),
            ],
        )

    def check_color_mode(self,switch, value):
        if value:
            self.theme_cls.theme_style = 'Dark'
            self.rebuild_dialog()
        else:
            self.theme_cls.theme_style = 'Light'
            self.rebuild_dialog()

    def get_date(self, date):
        print(date.day)

    def show_date_picker(self):
        date_dialog = MDDatePicker(callback=self.get_date)
        date_dialog.open()

    def show_alert_dialog(self):
        self.dialog.open()

    def back_to_main_menu(self):
        self.root.ids.screen_manager.current = 'main'

    def callback(self, instance_menu, instance_menu_item):
        if instance_menu_item.text == 'Settings':
            self.root.ids.screen_manager.current = 'settings'
        if instance_menu_item.text == 'About project':
            self.root.ids.screen_manager.current = 'about'
        instance_menu.dismiss()

    def build(self):
        return self.screen


MyApp().run()
