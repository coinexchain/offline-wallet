import ctypes
import json
import sys

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
import pexpect
import pyqrcode
import os

MODULE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
lib = ctypes.CDLL('./wallet.so')
signature_png_name = 'signature.png'
newAddress_png_name = 'newAddress.png'
address_png_name = 'address.png'


class Wallet(BoxLayout):
    lib.BearInit('tmp'.encode("utf-8"))
    pass


class Signature(BoxLayout):

    def stop_camera(self):
        self.ids['ZBarCam']


class Key(BoxLayout):
    pass


class Keys(BoxLayout):
    pass


class KeyQrCode(BoxLayout):
    pass


class DemoApp(App):
    key_resp = StringProperty("")
    keys_list = StringProperty()
    key_info = StringProperty()
    keys = ListProperty()
    keyName = ''
    keyPassword = ''
    chainId = ''
    accountNumber = ''
    sequence = ''

    def build(self):
        return Wallet()

    @staticmethod
    def build_signature_ui():
        return Signature()

    @staticmethod
    def build_wallet_ui():
        return Wallet()

    @staticmethod
    def build_key_ui():
        return Key()

    @staticmethod
    def build_keys_ui():
        return Keys()

    @staticmethod
    def build_key_qrcode():
        return KeyQrCode()

    def signature(self, s):
        print(s)
        print('unsigned json:')
        print(s.encode())
        print(self.keyName.encode())
        signed_str = self.sign(self.keyName.encode(), self.keyPassword.encode(), s.encode(),
                               self.chainId.encode(), int(self.accountNumber), int(self.sequence))
        self.create_qrcode(signed_str, signature_png_name)
        return signed_str

    @staticmethod
    def sign(key, password, s, chain_id, account_num, sequence):
        sign = lib.SignStdTx
        sign.restype = ctypes.c_char_p
        signature = sign(key, password, s, chain_id, account_num, sequence)
        return signature.decode('utf-8')

    # todo: repeat senario
    def add_key(self, name, password):
        print(name)
        print(password)
        name = name.encode()
        print(name)
        password = password.encode()
        create_key = lib.CreateKey
        create_key.restype = ctypes.c_char_p
        key = create_key(name, password, "", 0, 0)
        print(key)
        s = key.decode('utf-8')
        print(type(s))
        self.key_resp = s
        self.create_qrcode(s, newAddress_png_name)

    def get_key(self, name):
        list_keys = lib.ListKeys
        list_keys.restype = ctypes.c_char_p
        keys = list_keys()
        s = keys.decode('utf-8')
        parsed = json.loads(s)
        exist = False
        for key in parsed:
            if key['name'] == name:
                indent = json.dumps(key, indent=2, sort_keys=False)
                self.create_qrcode(indent, address_png_name)
                self.key_info = indent
                exist = True
        if not exist:
            self.key_info = 'This key is not exist'
        print(self.key_info)

    def list_keys(self):
        list_keys = lib.ListKeys
        list_keys.restype = ctypes.c_char_p
        keys = list_keys()
        s = keys.decode('utf-8')
        parsed = json.loads(s)
        print(parsed)
        out_to_file = json.dumps(parsed, indent=2, sort_keys=False)
        res = []
        for key in parsed:
            print(key)
            res.append({'name': key['name'], 'address': key['address']})
        indent = json.dumps(res, indent=2, sort_keys=False)
        self.keys_list = indent
        address_book = 'addressBook.txt'
        file = open(address_book, 'w')
        file.write(out_to_file)
        
    @staticmethod
    def create_qrcode(s, path):
        url = pyqrcode.create(s, error='L')
        url.png(path, scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])

    @staticmethod
    def remove_qrcode():
        if os.path.exists(signature_png_name):
            os.remove(signature_png_name)
        if os.path.exists(newAddress_png_name):
            os.remove(newAddress_png_name)
        if os.path.exists(address_png_name):
            os.remove(address_png_name)


if __name__ == '__main__':
    DemoApp().run()
