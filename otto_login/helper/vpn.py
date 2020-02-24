import osascript
import time

from otto_login import settings


def start():
    __run_osa(f'connect "{settings.vpn_config_name}"')

    while not check():
        time.sleep(2)


def stop():
    __run_osa(f'disconnect "{settings.vpn_config_name}"')


def check():
    out = __run_osa(f'get state of first configuration where name = "{settings.vpn_config_name}"')

    if out == settings.vpn_check_result:
        return True
    else:
        return False


def __run_osa(cmd):
    code, out, err = osascript.run(''
                                   'tell application "Tunnelblick"\n'
                                        f'{cmd}\n'
                                   'end tell'
                                   )
    if code == 0:
        return out
    else:
        raise err
