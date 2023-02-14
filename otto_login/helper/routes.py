import re
import socket
import subprocess
import dns.resolver

from otto_login import helper_functions as helper


def set_routes(a_records, sudo_pass, vpn_interface, default_interface):
    set_default_interface(default_interface, sudo_pass)

    for a_record in a_records:
        ip = resolv_a_record(a_record)
        if ip is not None:
            print(f'set vpn route for {ip}')
            # set_route(ip, vpn_interface, sudo_pass)


def resolv_a_record(record):
    try:
        answers = dns.resolver.query(record, 'CNAME')
        return answers
    except socket.gaierror:
        pass
    except Exception:
        raise


def set_default_interface(interface: str, sudo_pass: str):
    run_pipe_cmd(f'echo "{sudo_pass}" | sudo -S route change default -interface {interface}')


def set_route(ip: str, interface: str, sudo_pass: str):
    ip_type = 'host'

    if '/' in ip:
        ip_type = 'net'

    run_pipe_cmd(f'echo "{sudo_pass}" | sudo -S route add -{ip_type} {ip} -interface {interface}')


def get_default_interface():
    return re.search('interface: (.+)', helper.run_cmd(f'route get default')).group(1)


def run_pipe_cmd(cmd):
    try:
        proc = subprocess.Popen(cmd,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        stdout, _ = proc.communicate()

        return stdout
    except Exception:
        pass
