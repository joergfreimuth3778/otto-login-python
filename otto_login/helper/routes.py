import re
import socket
import subprocess

from otto_login import settings


def set_routes(a_records):
    vpn_interface = get_vpn_interface()
    for a_record in a_records:
        ip = resolv_a_record(a_record)
        if ip is not None:
            set_route(ip, vpn_interface)


def resolv_a_record(a_record):
    try:
        return socket.gethostbyname(a_record)
    except socket.gaierror:
        pass
    except:
        raise


def set_route(ip: str, interface: str):
    ip_type = 'host'

    if '/' in ip:
        ip_type = 'net'

    run_pipe_cmd(f'{settings.sudo_pass} | sudo -S route add -{ip_type} {ip} -interface {interface}')


def get_vpn_interface():
    return re.search('interface: (.+)',  run_cmd(f'route get {settings.otto_net}')).group(1)


def run_pipe_cmd(cmd):
    subprocess.Popen(cmd,
                     shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)


def run_cmd(cmd):
    try:
        process = subprocess.run(cmd.split(),
                                 check=True,
                                 stdout=subprocess.PIPE,
                                 universal_newlines=True,
                                 stderr=subprocess.DEVNULL)
        return process.stdout
    except:
        raise
