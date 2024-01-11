from argapp import App, Arg
from . import *

if DIR_UWS:
    from hardware import hardware
    from software import software
else:
    def hardware() -> 'list[Hardware] | Hardware':
        return []

    def software() -> 'list[Software]':
        return []


class AppShortcut(App):
    def __init__(
        self,
        app: 'App | str | None',
        name: 'str',
        help: 'str',
    ) -> None:
        self.__cmd = name
        if isinstance(app, str):
            super().__init__(help=f'Shortcut for: uniws {app} {name}\n{help}')
        else:
            super().__init__(name=name,
                             help=help)
            app.apps.append(self)

    def __call__(
        self,
        args: 'dict[Arg]' = None,
        apps: 'list[App]' = None,
    ) -> 'None':
        super().__call__(args, apps)
        if not DIR_UWS:
            raise RuntimeError('Not in the uniws workspace.')

    @property
    def cmd(self) -> 'str':
        return self.__cmd
