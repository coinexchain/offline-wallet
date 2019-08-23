import sys

from kivy.app import App
from kivy.lang import Builder

import os
import pexpect
import pyqrcode

MODULE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


class DemoApp(App):

    def build(self):
        return Builder.load_file(os.path.join(MODULE_DIRECTORY, "main.kv"))

    def signature(self, s):
        unsigned_str = self.build_sig(s)
        signed_str = self.sign(unsigned_str)
        self.create_qrcode(signed_str)
        return signed_str

    def build_sig(self, s):
        return 'un-signature'

    def sign(self, s):
        return 'signature'

    # todo: repeat senario
    def add_key(self, name, password):
        child = pexpect.spawnu('cetcli keys add ' + name)
        child.logfile = sys.stdout
        child.expect('Enter a passphrase to encrypt your key to disk:')
        child.sendline(password)
        child.expect('Repeat the passphrase:')
        child.sendline(password)
        child.expect('name')
        child.close()

    # todo: empty key senario
    def get_key(self, name):
        child = pexpect.spawnu('cetcli keys show ' + name)
        child.logfile = sys.stdout
        child.expect('name')
        child.close()

    # todo: empty keys senario
    def list_keys(self):
        child = pexpect.spawnu('cetcli keys list')
        child.logfile = sys.stdout
        child.expect('name')
        child.close()

    def create_qrcode(self, s):
        url = pyqrcode.create(s, error='L')
        url.png('1.png', scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])


if __name__ == '__main__':
    DemoApp().run()
