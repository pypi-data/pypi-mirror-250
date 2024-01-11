class Software:
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

    def fetch(self) -> 'None':
        raise NotImplementedError()

    def build(self) -> 'None':
        raise NotImplementedError()

    def install(self) -> 'None':
        raise NotImplementedError()

    def test(self) -> 'None':
        raise NotImplementedError()

    def release(self) -> 'None':
        raise NotImplementedError()

    def clean(self) -> 'None':
        raise NotImplementedError()

    def purge(self) -> 'None':
        raise NotImplementedError()
