from .lib import *


class Terminal:
    def __init__(
        self,
        name: 'str',
        help: 'str' = '',
    ) -> 'None':
        self.__name = name
        self.__help = help

    @property
    def name(self) -> 'str':
        return self.__name

    @property
    def help(self) -> 'str':
        return self.__help

    def onoff(self, state: 'bool') -> 'None':
        raise NotImplementedError()

    def get(self, src: 'str', dst: 'str') -> 'None':
        raise NotImplementedError()

    def put(self, src: 'str', dst: 'str') -> 'None':
        raise NotImplementedError()

    def sh(self, cmd: 'str') -> 'None':
        raise NotImplementedError()

    def watch(self) -> 'None':
        raise NotImplementedError()


class Hardware(Terminal):
    def __init__(
        self,
        name: 'str',
        ttys: 'list[Terminal]',
    ) -> 'None':
        super().__init__(name)
        self.__ttys = ttys or []

    @property
    def ttys(self) -> 'list[Terminal]':
        return self.__ttys

    def use(self, state: 'bool') -> 'None':
        raise NotImplementedError()
