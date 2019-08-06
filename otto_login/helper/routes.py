import socket
import os
import re
import subprocess


def resolv_a_record(a_record):
    try:
        return socket.gethostbyname(a_record)
    except socket.gaierror:
        pass
    except:
        raise


def set_default_interface(interface):
    run_cmd(f'sudo route change default -interface {interface}')


def get_default_route():
    return run_cmd('route -n get default')


def get_current_default_interface():
    current_default_route = get_default_route()
    return re.search('interface: (.+)', current_default_route).group(1)


def set_route(ip: str, interface: str):
    ip_type = 'host'

    if '/' in ip:
        ip_type = 'net'

    run_cmd(f'sudo route add -{ip_type} {ip} -interface {interface}')


def run_cmd(cmd):
    try:
        process = subprocess.run(cmd.split(), check=True, stdout=subprocess.PIPE, universal_newlines=True)
        return process.stdout
    except:
        raise
