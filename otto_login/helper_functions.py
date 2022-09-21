import json
import os
import subprocess

from otto_login import settings


def run_cmd(cmd):
    try:
        process = subprocess.run(cmd.split(),
                                 check=True,
                                 stdout=subprocess.PIPE,
                                 universal_newlines=True,
                                 stderr=subprocess.DEVNULL)
        return process.stdout
    except Exception as e:
        raise Exception(f"ERROR running {cmd}")


def get_secrets(cmd, data):
    one_password_session = None

    if not one_password_session:
        one_password_session = run_cmd(settings.op_signin)

    op_result = run_cmd(f"{cmd} {one_password_session}")

    return json.loads(op_result)[data].strip()


def check_tools(tools=settings.required_tools):
    for tool in tools:
        if os.system(f'which {tool} > /dev/null') > 0:
            print(f'{tool} not found, please install')
            exit(1)