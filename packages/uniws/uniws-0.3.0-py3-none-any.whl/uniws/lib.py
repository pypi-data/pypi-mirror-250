import os
import sys


def __pwd() -> 'str':
    return os.path.abspath(os.getenv('PWD'))


def __root() -> 'str':
    result = __pwd()
    while result != '/':
        if os.path.exists(f'{result}/.uniws'):
            return result
        result = os.path.dirname(result)
    return ''


DIR_PWD = __pwd()
DIR_UWS = __root()
DIR_UNI = f'{DIR_UWS}/.uniws'
DIR_BIN = f'{DIR_UWS}/bin'
DIR_ETC = f'{DIR_UWS}/etc'
DIR_LIB = f'{DIR_UWS}/lib'
DIR_TMP = f'{DIR_UWS}/tmp'

if DIR_UWS:
    sys.path.insert(0, f'{DIR_UWS}/.uniws')
