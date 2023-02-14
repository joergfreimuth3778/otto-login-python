import argparse

from otto_login import settings
from otto_login.helper import cpfw
from otto_login.helper import github
from otto_login.helper import vpn
from otto_login.helper import routes
from otto_login.helper.iam import IamHandler
from otto_login.helper.sts import StsHandler
from otto_login import helper_functions as helper
from otto_login.helper_functions import SecretsHelper


def run():
    helper.check_tools()

    parser = argparse.ArgumentParser(description='otto-login')

    parser.add_argument('-a', dest='aws', action='store_true', default=False, help='open aws sessions')
    parser.add_argument('-c', dest='checkout', action='store_true', default=False, help='checkout all git repos')
    parser.add_argument('-f', dest='firewall', action='store_true', default=False, help='firewall login')
    parser.add_argument('-r', dest='rotate', action='store_true', default=False, help='rotate access keys')
    parser.add_argument('-v', dest='vpn', action='store_true', default=False, help='connect to vpn')
    parser.add_argument('-s', dest='set_routes', action='store_true', default=False, help='set vpn routes')

    options = parser.parse_args()

    sts = StsHandler()
    secrets = SecretsHelper()

    if options.aws or options.rotate or options.firewall or options.set_routes:
        secrets.op_login()

    if (options.aws or options.rotate) and not sts.check_user_session_token():
        print(f'AWS Login')
        sts.save_session(secrets.get_secrets(settings.aws_otp_token, 'totp'))

    if options.rotate:
        print(f'Rotate AccessKeys')
        IamHandler(sts).rotate_access_keys()

    if options.checkout:
        print('Pull or clone repos')
        github.clone_repos()

    if options.vpn and not vpn.check():
        print("Start VPN")
        default_interface = routes.get_default_interface()
        vpn.start()
        vpn_interface = routes.get_default_interface()

        if options.set_routes:
            routes.set_routes([], secrets.get_secrets(settings.sudo_pass, 'value'), vpn_interface, default_interface)

    if options.firewall:
        print('Firewall Login')
        cpfw.login(secrets.get_secrets(settings.ocn_pass, 'value'))


if __name__ == '__main__':
    run()
