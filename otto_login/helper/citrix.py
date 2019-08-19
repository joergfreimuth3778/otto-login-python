import os
import time

from .routes import get_current_default_interface
from otto_login import settings


def start():
    kill_all_running_instances()
    run_cmd(f'nohup {settings.citrix_client} > /dev/null 2>&1 &')
    wait_for_connect()


def wait_for_connect():
    print('Wait for VPN-Connect ...')
    while settings.default_interface in get_current_default_interface():
        time.sleep(1)


def kill_all_running_instances():
    run_cmd(f"killall {settings.citrix_client.split('/')[-1]} > /dev/null 2>&1")


def run_cmd(cmd):
    try:
        os.system(cmd)
    except:
        raise
