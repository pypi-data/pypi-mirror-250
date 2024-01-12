# PYTHON_ARGCOMPLETE_OK

from .app import *


class AppUniws(App):
    def __init__(self) -> 'None':
        super().__init__(name='uniws',
                         help='The main uniws application.')
        self.apps.append(AppInit())
        self.apps.append(AppHardware())
        self.apps.append(AppSoftware())


def uniws() -> 'None':
    AppUniws()()


def uhc() -> 'None':
    AppHardware.connect(False)()


def uhp() -> 'None':
    AppHardware.power(False)()


def uhu() -> 'None':
    AppHardware.upload(False)()


def uhd() -> 'None':
    AppHardware.download(False)()


def uhs() -> 'None':
    AppHardware.shell(False)()


def uhw() -> 'None':
    AppHardware.watch(False)()


def uha() -> 'None':
    AppHardware.action(False)()


def usf() -> 'None':
    AppSoftware.fetch(False)()


def usb() -> 'None':
    AppSoftware.build(False)()


def usi() -> 'None':
    AppSoftware.install(False)()


def ust() -> 'None':
    AppSoftware.test(False)()


def usr() -> 'None':
    AppSoftware.release(False)()


def usc() -> 'None':
    AppSoftware.clean(False)()


def usp() -> 'None':
    AppSoftware.purge(False)()


def usa() -> 'None':
    AppSoftware.action(False)()
