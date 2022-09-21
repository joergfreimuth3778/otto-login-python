import subprocess
import json

from otto_login import settings
from otto_login import helper_functions as helper


def login(one_password_session):
    helper.run_cmd(f'{settings.firewall_login_tool} '
                   f'--url {settings.firewall_url} '
                   f'--user {settings.ocn_user} '
                   f'--password {ocn_password(one_password_session)} '
                   f'--insecure')


def ocn_password(one_password_session):
    one_password_result = json.loads(helper.run_cmd(f"{settings.ocn_pass} {one_password_session}"))
    return one_password_result['value']
