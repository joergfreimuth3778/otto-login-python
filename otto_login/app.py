import argparse
import os

from otto_login import settings
from otto_login.helper import cpfw
from otto_login.helper import github
from otto_login.helper import vpn
from otto_login.helper.iam import IamHandler
from otto_login.helper.sts import StsHandler
from otto_login import helper_functions as helper


def run():
    check_tools()

    parser = argparse.ArgumentParser(description='otto-login')

    parser.add_argument('-a', dest='aws', action='store_true', default=False, help='open aws sessions')
    parser.add_argument('-c', dest='checkout', action='store_true', default=False, help='checkout all git repos')
    parser.add_argument('-f', dest='firewall', action='store_true', default=False, help='firewall login')
    parser.add_argument('-r', dest='rotate', action='store_true', default=False, help='rotate access keys')
    parser.add_argument('-v', dest='vpn', action='store_true', default=False, help='connect to vpn')

    options = parser.parse_args()
    one_password_session = None
    sts = StsHandler()

    if (options.aws or options.rotate) and not sts.check_user_session_token():
        print(f'AWS-Login')
        one_password_session = helper.run_cmd(settings.op_signin)
        sts.save_session(one_password_session)

    if options.rotate:
        print(f'Rotate AccessKeys')
        IamHandler(sts).rotate_access_keys()

    if options.checkout:
        print('Pull or clone git repos')
        github.clone_github_repos()

    if options.firewall:
        print('Firewall-Login')
        if not one_password_session:
            one_password_session = helper.run_cmd(settings.op_signin)

        check_tools({settings.firewall_login_tool})
        cpfw.login(one_password_session)

    if options.vpn and not vpn.check():
        print("Start VPN")
        vpn.start()


def check_tools(tools=settings.required_tools):
    for tool in tools:
        if os.system(f'which {tool} > /dev/null') > 0:
            print(f'{tool} not found, please install')
            exit(1)


if __name__ == '__main__':
    run()
