from argapp import App

from uniws.app import App
from .app import *


class AppShortcutSoftware(AppShortcut):
    def __init__(
        self,
        app: 'App | None',
        name: 'str',
    ) -> None:
        app = app or 'sw'
        super().__init__(app, name, f'{name.capitalize()} software.')
        self.sw: dict[str, Software] = {}
        for x in software():
            if getattr(type(x), self.cmd, None) != getattr(Software, self.cmd, None):
                self.sw[x.name] = x
        if self.sw:
            choices = {x.name: x.help for x in self.sw.values()}
            self.arg = Arg(help=f'Software to {self.cmd}.',
                           count='?',
                           choices=choices,
                           default=next(iter(choices)),
                           name='SW')
        else:
            self.arg = Arg(help=f'Software to {self.cmd} (none available).',
                           count='?',
                           name='SW')
        self.args.append(self.arg)

    def __call__(
        self,
        args: 'dict[Arg]' = None,
        apps: 'list[App]' = None,
    ) -> 'None':
        super().__call__(args, apps)
        if not self.sw:
            raise RuntimeError(f'There is no software to {self.cmd}.')
        getattr(self.sw[args[self.arg]], self.cmd)()


class AppShortcutSoftwareFetch(AppShortcutSoftware):
    def __init__(self, app: 'App | None') -> 'None':
        super().__init__(app=app,
                         name='fetch')


class AppShortcutSoftwareBuild(AppShortcutSoftware):
    def __init__(self, app: 'App | None') -> 'None':
        super().__init__(app=app,
                         name='build')


class AppShortcutSoftwareInstall(AppShortcutSoftware):
    def __init__(self, app: 'App | None') -> 'None':
        super().__init__(app=app,
                         name='install')


class AppShortcutSoftwareTest(AppShortcutSoftware):
    def __init__(self, app: 'App | None') -> 'None':
        super().__init__(app=app,
                         name='test')


class AppShortcutSoftwareRelease(AppShortcutSoftware):
    def __init__(self, app: 'App | None') -> 'None':
        super().__init__(app=app,
                         name='release')


class AppShortcutSoftwareClean(AppShortcutSoftware):
    def __init__(self, app: 'App | None') -> 'None':
        super().__init__(app=app,
                         name='clean')


class AppShortcutSoftwarePurge(AppShortcutSoftware):
    def __init__(self, app: 'App | None') -> 'None':
        super().__init__(app=app,
                         name='purge')


class AppSoftware(App):
    def __init__(self, app: 'App | None') -> 'None':
        super().__init__(app=app,
                         name='sw',
                         help='Manipulate software.')
        AppShortcutSoftwareFetch(self)
        AppShortcutSoftwareBuild(self)
        AppShortcutSoftwareInstall(self)
        AppShortcutSoftwareTest(self)
        AppShortcutSoftwareRelease(self)
        AppShortcutSoftwareClean(self)
        AppShortcutSoftwarePurge(self)
