import os
import time

import osascript

from otto_login import settings


def start():
    if not check():
        run_osa()

    while not check():
        print("Waiting for connection")
        time.sleep(2)


def check():
    response = os.system(f"ping -t 1 -c 1 {settings.nameserver} > /dev/null")
    if response == 0:
        return True
    else:
        return False


def run_osa():
    code, out, err = osascript.run(''
                                    'tell application "System Events" to tell process "GlobalProtect"\n'
                                        'click menu bar item 1 of menu bar 2\n'
                                        'click button 2 of window 1\n'
                                    'end tell'
                                   )
    if code == 0:
        return out
    else:
        raise Exception(err)
