import argparse
import os

from otto_login.helper import routes
from otto_login.helper import vpn
from otto_login.helper import github
from otto_login.helper import cpfw

from .helper.sts import StsHandler
from .helper.iam import IamHandler
from .helper.route53 import Route53Handler
from .helper.ec2 import Ec2Handler

from otto_login import settings


def run():
    check_tools()

    parser = argparse.ArgumentParser(description='otto-login')

    parser.add_argument('-v', dest='vpn', action='store_true', default=False, help='connect to vpn')
    parser.add_argument('-a', dest='aws', action='store_true', default=False, help='open aws sessions')
    parser.add_argument('-r', dest='rotate', action='store_true', default=False, help='rotate access keys')
    parser.add_argument('-s', dest='security_group', action='store_true', default=False, help='add own ip to alb-internal-sg')
    parser.add_argument('-o', dest='record_file', default=None, help='get ARecords from file')
    parser.add_argument('-f', dest='firewall', action='store_true', default=False, help='firewall login')
    parser.add_argument('-c', dest='checkout', action='store_true', default=False, help='checkout all git repos')
    parser.add_argument('-d', dest='routes', action='store_true', default=False, help='change default route')

    options = parser.parse_args()

    sts = StsHandler()

    if options.aws:
        aws_root_session, aws_root_credentials = sts.get_root_session()

        sessions_to_save = {
            settings.root_session_profile: aws_root_credentials
        }

        for env, account in settings.accounts.items():
            print(f'Create AWS-Session for {env}')
            assume_credentials = sts.assume_role(aws_root_session, account)['Credentials']
            run_session = sts.get_credentials_session(assume_credentials)
            ec2 = Ec2Handler(run_session, env)

            sessions_to_save[env] = run_session.get_credentials()

            if options.routes:
                print(f'Get A-Records from {env}')
                routes.set_routes(Route53Handler(run_session).arecords(env))

            if options.security_group:
                print(f'Add own ip to {ec2.security_group_name()}')
                ec2.update_security_group()

        sts.save_sessions(sessions_to_save)

        if options.rotate:
            print(f'Rotate AccessKeys')
            IamHandler(aws_root_session).rotate_access_keys()

    if options.record_file:
        if vpn.check():
            print(f'Get A-Records from {options.record_file}')
            routes.set_routes(records_from_file(options.record_file))
        else:
            print('No active VPN-Connection')

    if options.vpn:
        print(f'Start VPN')
        vpn.start()
        
    if options.checkout:
        print('Pull or clone git repos')
        github.clone_github_repos()

    if options.firewall:
        check_tools({settings.firewall_login_tool})
        cpfw.login()


def check_tools(tools=settings.required_tools):
    for tool in tools:
        if os.system(f'which {tool} > /dev/null') > 0:
            print(f'{tool} not found, please install')
            exit(1)


def records_from_file(file):
    result = list()
    with open(file) as fp:
        for _, line in enumerate(fp):
            result.append(line.strip())

    return result
