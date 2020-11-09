from kivymd.app import MDApp
from kivy.lang import Builder


class MyApp(MDApp):

    def build(self):
        return Builder.load_string(
            '''
BoxLayout:
    orientation:'vertical'

    MDToolbar:
        title: 'Shopping list'

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
        )


MyApp().run()