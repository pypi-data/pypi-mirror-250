from .app import *


class AppShortcutHardware(AppShortcut):
    def __init__(
        self,
        app: 'App | None',
        name: 'str',
        help: 'str',
        tty: 'bool',
    ) -> None:
        app = app or 'hw'
        super().__init__(app, name, help)
        self.eargs = []
        self.tty = tty
        self.hw: dict[str, Hardware] = {}
        self.error = None
        self.arg = None
        hw = hardware()
        if tty:
            if not isinstance(hw, Hardware):
                ttys = []
                self.error = RuntimeError('Not using any hardware.')
            else:
                ttys = [x for x in hw.ttys]
                ttys.insert(0, hw)
            for x in ttys:
                if getattr(type(x), self.name, None) != getattr(Hardware, self.name, None):
                    self.hw[x.name] = x
            if self.name in self.hw:
                self.hw.pop(self.name)
                self.hw['self'] = self.hw
        else:
            if not hw:
                self.error = RuntimeError('No hardware available.')
        if len(self.hw) > 1:
            choices = {x.name: x.help for x in self.hw.values()}
            name = 'TTY' if tty else 'HW'
            help = 'Terminal' if tty else 'Hardware'
            count = None
            default = None
            if 'self' in self.hw:
                count = '?'
                default = 'self'
            self.arg = Arg(app=self,
                           count=count,
                           choices=choices,
                           default=default,
                           help=f'{help} to use.',
                           name=name)

    def __call__(
        self,
        args: 'dict[Arg]' = None,
        apps: 'list[App]' = None,
    ) -> 'None':
        super().__call__(args, apps)
        if self.error:
            raise self.error
        if self.arg:
            hw = self.hw[args[self.arg]]
        else:
            hw = next(iter(self.hw.values()))
        eargs = [args[x] for x in self.eargs]
        getattr(hw, self.cmd)(*eargs)


class AppShortcutHardwareUse(AppShortcutHardware):
    def __init__(self, app: 'App | None') -> None:
        super().__init__(app=app,
                         name='use',
                         help='Use the hardware: attach or detach.',
                         tty=False)
        self.eargs.append(Arg(app=self,
                              sopt='d',
                              lopt='detach',
                              help='Detach if attached.',
                              count=0,
                              default=True))


class AppShortcutHardwareOnoff(AppShortcutHardware):
    def __init__(self, app: 'App | None') -> None:
        super().__init__(app=app,
                         name='onoff',
                         help='Power cycle the hardware.',
                         tty=True)
        self.eargs.append(Arg(app=self,
                              sopt='o',
                              lopt='off',
                              help='Power off only.',
                              count=0))


class AppShortcutHardwareSh(AppShortcutHardware):
    def __init__(self, app: 'App | None') -> None:
        super().__init__(app=app,
                         name='sh',
                         help='Execute a command or interact with the shell.',
                         tty=True)
        self.eargs.append(Arg(app=self,
                              name='CMD',
                              help='A command to run. Interactive session if not set.',
                              count='?'))


class AppShortcutHardwareGet(AppShortcutHardware):
    def __init__(self, app: 'App | None') -> None:
        super().__init__(app=app,
                         name='get',
                         help='Copy from the hardware to the local machine.',
                         tty=True)
        self.eargs.append(Arg(app=self,
                              name='SRC',
                              help='The source path.'))
        self.eargs.append(Arg(app=self,
                              name='DST',
                              help='The destination path.'))


class AppShortcutHardwarePut(AppShortcutHardware):
    def __init__(self, app: 'App | None') -> None:
        super().__init__(app=app,
                         name='put',
                         help='Copy from the local machine to the hardware.',
                         tty=True)
        self.eargs.append(Arg(app=self,
                              name='SRC',
                              help='The source path.'))
        self.eargs.append(Arg(app=self,
                              name='DST',
                              help='The destination path.'))


class AppShortcutHardwareWatch(AppShortcutHardware):
    def __init__(self, app: 'App | None') -> None:
        super().__init__(app=app,
                         name='watch',
                         help='Watch the live stream.',
                         tty=True)


class AppHardware(App):
    def __init__(self, app: 'App | None') -> 'None':
        super().__init__(app=app,
                         name='hw',
                         help='Manipulate hardware.')
        AppShortcutHardwareUse(self)
        AppShortcutHardwareOnoff(self)
        AppShortcutHardwareSh(self)
        AppShortcutHardwareGet(self)
        AppShortcutHardwarePut(self)
        AppShortcutHardwareWatch(self)
