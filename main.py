import ctypes
import sys

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
import pexpect
import pyqrcode
import os

MODULE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


class Wallet(BoxLayout):
    pass


class Signature(BoxLayout):

    def stop_camera(self):
        self.ids['ZBarCam']


class Key(BoxLayout):
    pass


class Keys(BoxLayout):
    pass


class DemoApp(App):

    key_resp = StringProperty("")
    keys_list = StringProperty()

    def build(self):
        return Wallet()

    def build_signature_ui(self):
        return Signature()

    def build_wallet_ui(self):
        return Wallet()

    def build_key_ui(self):
        return Key()

    def build_keys_ui(self):
        return Keys()

    def signature(self, s):
        print(s)
        signed_str = self.sign("dd", "12345678", s[2:len(s)-1])
        self.create_qrcode(signed_str, '1.png')
        return signed_str

    def sign(self, key, password, s):
        lib = ctypes.CDLL('./wallet.so')
        sign = lib.Sign
        sign.restype = ctypes.c_char_p
        signature = sign(key, password, s)
        return signature.decode('utf-8')

    # todo: repeat senario
    def add_key(self, name, password):
        lib = ctypes.CDLL('./wallet.so')
        lib.BearInit('tmp'.encode("utf-8"))
        create_key = lib.CreateKey
        create_key.restype = ctypes.c_char_p
        key = create_key(name, password, "", 0, 0)
        print(key)
        s = key.decode('utf-8')
        print(type(s))
        self.key_resp = s
        self.create_qrcode(s, '2.png')

    # todo: empty key senario
    def get_key(self, name):
        child = pexpect.spawnu('cetcli keys show ' + name)
        child.logfile = sys.stdout
        child.expect('name')
        child.close()

    # todo: empty keys senario
    def list_keys(self):
        lib = ctypes.CDLL('./wallet.so')
        print(lib)
        list_keys = lib.ListKeys
        print(list_keys)
        list_keys.restype = ctypes.c_char_p
        keys = list_keys()
        print(keys)
        self.keys_list = keys.decode('utf-8')

    def create_qrcode(self, s, path):
        url = pyqrcode.create(s, error='L')
        url.png(path, scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])

    def remove_qrcode(self):
        os.remove('1.png')


if __name__ == '__main__':
    DemoApp().run()
