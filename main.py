from kivy.app import App
from kivy.lang import Builder

import os


MODULE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


class DemoApp(App):

    def build(self):
        return Builder.load_file("/Users/helldealer/offline-wallet/main.kv")

    def signature(self):
        s = '"8","coinexdex-test1","200000000","cet","1000000","create gte order",1,"market/MsgCreateOrder","10000",' \
            '2,"61",1,543973922",coinex1x6rhu5m53fw8qgpwuljauaptvxyur57zym4jly","5945",2,3","abc/cet","5945" '
        print s.split(',')
        return 'sig'


if __name__ == '__main__':
    DemoApp().run()
