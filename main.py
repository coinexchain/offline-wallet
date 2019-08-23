from kivy.app import App
from kivy.lang import Builder

import os


MODULE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


class DemoApp(App):

    def build(self):
        return Builder.load_file("/Users/helldealer/offline-wallet/main.kv")


if __name__ == '__main__':
    DemoApp().run()
