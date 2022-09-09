import argparse
import os
import subprocess

from otto_login import settings
from otto_login.helper import cpfw
from otto_login.helper import github
from otto_login.helper import vpn
from otto_login.helper.iam import IamHandler
from otto_login.helper.sts import StsHandler


def run():
    check_tools()

    parser = argparse.ArgumentParser(description='otto-login')

    parser.add_argument('-v', dest='vpn', action='store_true', default=False, help='connect to vpn')
    parser.add_argument('-a', dest='aws', action='store_true', default=False, help='open aws sessions')
    parser.add_argument('-r', dest='rotate', action='store_true', default=False, help='rotate access keys')
    parser.add_argument('-f', dest='firewall', action='store_true', default=False, help='firewall login')
    parser.add_argument('-c', dest='checkout', action='store_true', default=False, help='checkout all git repos')

    options = parser.parse_args()

    if options.aws or options.firewall:
        one_password_session = run_cmd(settings.op_signin)

    if options.aws or options.rotate:
        sts = StsHandler()
        aws_root_session, aws_root_credentials = sts.get_root_session(one_password_session)

    if options.vpn:
        print("Start VPN")
        vpn.start()

    if options.aws:
        sessions_to_save = {
            settings.root_session_profile: aws_root_credentials
        }

        for env, account in settings.accounts.items():
            print(f'Create AWS-Session for {env}')
            assume_credentials = sts.assume_role(aws_root_session, account)['Credentials']
            run_session = sts.get_credentials_session(assume_credentials)

            sessions_to_save[env] = run_session.get_credentials()

        sts.save_sessions(sessions_to_save)

    if options.rotate:
        print(f'Rotate AccessKeys')
        IamHandler(aws_root_session).rotate_access_keys()
        
    if options.checkout:
        print('Pull or clone git repos')
        github.clone_github_repos()

    if options.firewall:
        check_tools({settings.firewall_login_tool})
        cpfw.login(one_password_session)


def check_tools(tools=settings.required_tools):
    for tool in tools:
        if os.system(f'which {tool} > /dev/null') > 0:
            print(f'{tool} not found, please install')
            exit(1)


def run_cmd(cmd):
    print(cmd)
    try:
        process = subprocess.run(cmd.split(),
                                 check=True,
                                 stdout=subprocess.PIPE,
                                 universal_newlines=True,
                                 stderr=subprocess.DEVNULL)
        return process.stdout
    except Exception as e:
        pass


if __name__ == '__main__':
    run()