import sys

from kivy.app import App
from kivy.lang import Builder

import os
import pexpect

MODULE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


class DemoApp(App):

    def build(self):
        return Builder.load_file("/Users/helldealer/offline-wallet/main.kv")

    def signature(self, s):
        self.build_sig(s)

        return 'sig'

    def build_sig(self, s):
        pass

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


if __name__ == '__main__':
    DemoApp().run()
