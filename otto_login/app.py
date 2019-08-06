import argparse

from .helper.login import LoginHandler
from .helper.route53 import Route53Handler
from .helper.routes import resolv_a_record
from .helper.routes import get_current_default_interface
from .helper.routes import set_default_interface
from .helper.routes import set_route

from otto_login import settings


def run():
    parser = argparse.ArgumentParser(description='otto-login')

    parser.add_argument('-v', dest='vpn', action='store_true', default=False, help='connect to vpn')
    parser.add_argument('-r', dest='rotate', action='store_true', default=False, help='rotate access keys')
    parser.add_argument('-a', dest='aws_arecords', action='store_true', default=False, help='get aws ARecords')
    parser.add_argument('-o', dest='record_file', default=None, help='get ARecords from file')
    parser.add_argument('-f', dest='firewall', action='store_true', default=False, help='firewall login')

    options = parser.parse_args()

    login_handler = LoginHandler()

    if login_handler.check_session_token():
        assume_session = login_handler.get_profile_session(settings.intermediate_profile)
    else:
        token = input("Enter MFA-Token: ")
        session_credentials = login_handler.get_session_token(token)['Credentials']
        assume_session = login_handler.get_credentials_session(session_credentials)

    vpn_interface = get_current_default_interface()
    set_default_interface(settings.default_interface)

    for env, account in settings.accounts.items():
        assume_credentials = login_handler.assume_role(assume_session, account)['Credentials']
        run_session = login_handler.get_credentials_session(assume_credentials)

        for a_record in Route53Handler(run_session).arecords(env):
            ip = resolv_a_record(a_record)
            if ip is not None:
                set_route(ip, vpn_interface)

