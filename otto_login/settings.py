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

firewall_login_tool = 'cpfw-login'

required_tools = ('route', 'aws', 'git', 'security', firewall_login_tool, 'op')

github_org = 'otto-ec'
github_team_id = 2770943
github_base = 'github.com'
github_api = f'https://api.{github_base}'
github_repo_prefix = 'tr_'

firewall_domain = 'fwauth.ov.otto.de'
firewall_url = f'https://{firewall_domain}'

local_repo_path = f'{os.environ["REPO_DIR"]}'
archived_repo_path = f'{local_repo_path}/archived'


ocn_pass = 'security find-generic-password -j ocn-pwd -w'
github_token = 'security find-generic-password -j github -w'
sudo_pass = 'security find-generic-password -j sudo -w'
op_signin = 'op signin my --raw'
op_aws_token = 'op get totp AWS-Otto --session '
vpn_check_result = 'CONNECTED'
vpn_config_name = 'ottogroup'
