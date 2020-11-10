from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.menu import MDDropdownMenu

KV =  '''
BoxLayout:
    orientation:'vertical'

    MDToolbar:
        id: button
        title: 'Shopping list'
        right_action_items: [["dots-vertical", lambda x: app.menu.open()]]
    
    MDScreen:
        name: "screen_1"

    MDBottomNavigation:

        MDBottomNavigationItem:
            name: 'screen 1'
            text: 'History'
            icon: 'language-python'

            MDLabel:
                text: 'History purchase'
                halign: 'center'

        MDBottomNavigationItem:
            name: 'screen 2'
            text: 'Active'
            icon: 'language-cpp'

            MDLabel:
                text: 'Active items'
                halign: 'center'
'''

class MyApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        menu_items = [
            {"text": 'Settings'},{"text": 'About project'}
        ]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.button,
            items=menu_items,
            width_mult=4
        )
        self.menu.bind(on_release=self.callback)

    def callback(self,instance_menu, instance_menu_item):
        print(instance_menu, instance_menu_item.text)

    def build(self):
        return self.screen


MyApp().run()