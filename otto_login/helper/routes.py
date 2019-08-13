import re
import socket
import subprocess


def set_routes(a_records, interface):
    for a_record in a_records:
        ip = resolv_a_record(a_record)
        if ip is not None:
            set_route(ip, interface)


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
    return re.search('interface: (.+)',  get_default_route()).group(1)


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
