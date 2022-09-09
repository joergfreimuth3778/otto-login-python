import os

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

required_tools = ('aws', 'git', firewall_login_tool, 'op')

github_org = 'otto-ec'
github_team_id = 2770943
github_base = 'github.com'
github_api = f'https://api.{github_base}'
github_repo_prefix = 'tr_'

firewall_domain = 'fwauth.ov.otto.de'
firewall_url = f'https://{firewall_domain}'
nameserver = '10.79.255.100'

local_repo_path = f'{os.environ["HOME"]}/Otto/workspace/tracking'
archived_repo_path = f'{local_repo_path}/archived'
files_to_link = [
    f"{local_repo_path}/tools/javaagent",
    f"{local_repo_path}/editor-config/.editorconfig",
]

op_signin = 'op signin --raw'
ocn_pass = 'op item get OCN --fields password --format json --session'
aws_otp_token = 'op item get AWS-Otto --field type=otp --format json --session'
github_token = os.environ["GITHUB_TOKEN"]
