from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

import filedatacomponents
import searchcomponents
'''
The root widget for all kivy components
'''


class RootLayout(FloatLayout):

    search_display = None
    file_data_display = None

    def __init__(self, **kwargs):
        super(RootLayout, self).__init__(**kwargs)

        Window.size = (1920, 1080)

        self.search_display = searchcomponents.SearchComponents()
        self.file_data_display = filedatacomponents.FileDataComponents()

        self.add_widget(self.search_display)
        self.add_widget(self.file_data_display)


root = RootLayout()
