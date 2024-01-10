# PYTHON_ARGCOMPLETE_OK

from .app_init import *
from .app_hw import *
from .app_sw import *


class AppUniws(App):
    def __init__(self) -> 'None':
        super().__init__(name='uniws',
                         help='The main uniws application.')
        AppInit(self)
        AppHardware(self)
        AppSoftware(self)


def uniws() -> 'None':
    AppUniws()()


def uhu() -> 'None':
    AppShortcutHardwareUse(None)()


def uho() -> 'None':
    AppShortcutHardwareOnoff(None)()


def uhs() -> 'None':
    AppShortcutHardwareSh(None)()


def uhg() -> 'None':
    AppShortcutHardwareGet(None)()


def uhp() -> 'None':
    AppShortcutHardwarePut(None)()


def uhw() -> 'None':
    AppShortcutHardwareWatch(None)()


def usf() -> 'None':
    AppShortcutSoftwareFetch(None)()


def usb() -> 'None':
    AppShortcutSoftwareBuild(None)()


def usi() -> 'None':
    AppShortcutSoftwareInstall(None)()


def ust() -> 'None':
    AppShortcutSoftwareTest(None)()


def usr() -> 'None':
    AppShortcutSoftwareRelease(None)()


def usc() -> 'None':
    AppShortcutSoftwareClean(None)()


def usp() -> 'None':
    AppShortcutSoftwarePurge(None)()
