from argapp import App, Arg

from .app import *


class AppInit(App):
    def __init__(self, app: 'App | None') -> 'None':
        super().__init__(app=app,
                         name='init',
                         help='Initialize an empty uniws workspace.')
        self.arg_remote = Arg(app=self,
                              name='URI',
                              sopt='r',
                              lopt='remote',
                              help='A Git remote to set as the origin.')
        self.arg_branch = Arg(app=self,
                              name='NAME',
                              sopt='b',
                              lopt='branch',
                              help='A Git branch to set as main.')
        self.arg_dir = Arg(app=self,
                           name='DIR',
                           count='?',
                           default='.',
                           help=str('A non-existing or empty directory. '
                                    'Defaults to the current one.'))

    def __call__(
        self,
        args: 'dict[Arg]' = None,
        apps: 'list[App]' = None,
    ) -> 'None':
        super().__call__(args, apps)
        dir = os.path.abspath(args[self.arg_dir])
        if os.path.exists(dir):
            if os.path.isdir(dir):
                if len(os.listdir(dir)) != 0:
                    raise RuntimeError(f'Directory not empty: {dir}')
            else:
                raise RuntimeError(f'Not a directory: {dir}')
        else:
            os.makedirs(dir, 0o755)
        branch = args[self.arg_branch]
        branch = f'-b {branch}' if branch else ''
        remote = args[self.arg_remote]
        remote = f'git remote add origin {remote}' if remote else 'true'
        sh(f'true'
           f' && cp -RaT {os.path.dirname(__file__)}/template {dir}'
           f' && cd {dir}'
           f' && git init {branch}'
           f' && {remote}'
           f' && git add -A'
           f' && git commit -m "Initial commit"'
           f';')
