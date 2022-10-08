import json
import os
import subprocess

from otto_login import settings


class SecretsHelper:
    def __init__(self, ):
        self.one_password_session = None

    def op_login(self):
        if not self.one_password_session:
            self.one_password_session = run_cmd(settings.op_signin)

    def get_secrets(self, cmd, data):
        op_result = run_cmd(f"{cmd} {self.one_password_session}")

        return json.loads(op_result)[data].strip()


def run_cmd(cmd, return_cmd=False, stderr=subprocess.STDOUT):
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=stderr)

    if return_cmd:
        return proc

    stdout, _ = proc.communicate()

    if proc.returncode != 0:
        print(f"ERROR running cmd {cmd.split()[0]}\n"
              f"{stdout.decode()}")
        exit(1)

    return stdout.decode().strip()


def check_tools(tools=settings.required_tools):
    for tool in tools:
        if os.system(f'which {tool} > /dev/null') > 0:
            print(f'{tool} not found, please install')
            exit(1)
