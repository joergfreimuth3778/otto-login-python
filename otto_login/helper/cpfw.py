from otto_login import settings
from otto_login import helper_functions as helper


def login(password):
    print(helper.run_cmd(f'{settings.firewall_login_tool} '
                         f'--url {settings.firewall_url} '
                         f'--user {settings.ocn_user} '
                         f'--password {password} '
                         f'--insecure'))
