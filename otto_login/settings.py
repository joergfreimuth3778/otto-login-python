import os

otto_net = '10.0.0.0/8'

ec_account = '027617375449'
accounts = {
    'live': 726963838652,
    'develop': 973172234831,
    'infra': 967223975844,
}

region = 'eu-central-1'
ocn_user = os.environ["OCN_USER"]
mfa_device = f'arn:aws:iam::{ec_account}:mfa/{ocn_user}'
root_session_profile = 'session-token'
credentials_file = f'{os.environ["HOME"]}/.aws/credentials'
role = 'admin'

required_tools = ('route', 'aws', 'git')

github_org = 'otto-ec'
github_team_id = 2770943
github_base = 'github.com'
github_api = f'https://api.{github_base}'
github_repo_prefix = 'tr_'

firewall_domain = 'fwauth.ov.otto.de'
firewall_url = f'https://{firewall_domain}'

local_repo_path = f'{os.environ["HOME"]}/Otto/workspace/tracking'

firewall_login_tool = 'cpfw-login'

ocn_pass = 'security find-generic-password -j ocn -w'
github_token = 'security find-generic-password -j github -w'
vpn_check_result = 'CONNECTED'
vpn_config_name = 'ottogroup'
