from kivy.app import App

import rootlayout
import socketcomm

'''
Default kivy configuration
'''


class InterfaceGUIApplication(App):

    def build(self):
        return rootlayout.root


'''
Runs main application
'''
if __name__ == '__main__':
    socketcomm.open_socket(5119)
    socketcomm.base_directory = socketcomm.set_base_directory()
    InterfaceGUIApplication().run()
