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
        unsigned_str = self.build_sig(s)
        signed_str = self.sign(unsigned_str)
        self.create_qrcode(signed_str, '1.png')
        return signed_str

    def build_sig(self, s):
        return 'un-signature'

    def sign(self, s):
        return 'show signature output'

    # todo: repeat senario
    def add_key(self, name, password):
        child = pexpect.spawnu('cetcli keys add ' + name)
        child.logfile = open('mylog.txt', 'w')
        child.expect('Enter a passphrase to encrypt your key to disk:')
        child.sendline(password)
        child.expect('Repeat the passphrase:')
        child.sendline(password)
        child.expect('name')
        child.close()
        f = open('mylog.txt', 'r')
        s = f.readlines()[5:9]
        self.key_resp = ''.join(s)
        f.close()
        os.remove('mylog.txt')
        os.remove('2.log')
        self.create_qrcode(str(s), '2.png')


    # todo: empty key senario
    def get_key(self, name):
        child = pexpect.spawnu('cetcli keys show ' + name)
        child.logfile = sys.stdout
        child.expect('name')
        child.close()

    # todo: empty keys senario
    def list_keys(self):
        child = pexpect.spawnu('cetcli keys list')
        child.logfile = open('mylog.txt', 'w')
        child.expect('name')
        child.close()
        f = open('mylog.txt', 'r')
        self.keys_list = ''.join(f.readlines())
        f.close()
        os.remove('mylog.txt')

    def create_qrcode(self, s, path):
        url = pyqrcode.create(s, error='L')
        url.png(path, scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])

    def remove_qrcode(self):
        os.remove('1.png')


if __name__ == '__main__':
    DemoApp().run()
