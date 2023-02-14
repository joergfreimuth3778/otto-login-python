import os

ec_account = '027617375449'
ocn_user = os.environ["OCN_USER"]
mfa_device = f'arn:aws:iam::{ec_account}:mfa/{ocn_user}'
user_session_profile = 'session-token'

firewall_login_tool = 'cpfw-login'
required_tools = ('aws', 'git', firewall_login_tool, 'op')

github_org = 'otto-ec'
github_team_id = 2770943
github_base = 'github.com'
github_api = f'https://api.{github_base}'
github_repo_prefix = 'tr_'
github_token = os.environ["GITHUB_TOKEN"]
local_repo_path = os.environ["REPO_DIR"]
archived_repo_path = f'{local_repo_path}/archived'
files_to_link = [
    f"{local_repo_path}/tools/javaagent",
    f"{local_repo_path}/editor-config/.editorconfig",
]

firewall_domain = 'fwauth.ov.otto.de'
firewall_url = f'https://{firewall_domain}'
nameserver = '10.79.255.100'
otto_net = '10.0.0.0/8'

op_signin = 'op signin --raw'
ocn_pass = 'op item get OCN --fields password --format json --session'
sudo_pass = 'op item get MacLogin --fields password --format json --session'
aws_otp_token = 'op item get AWS-Otto --field type=otp --format json --session'

vpn_routes = [
    'alb-infra-internal-962665732.eu-central-1.elb.amazonaws.com',
    'alb-develop-internal-1166730190.eu-central-1.elb.amazonaws.com',
    'alb-develop-external-83862302.eu-central-1.elb.amazonaws.com',
    'alb-live-external-1443269452.eu-central-1.elb.amazonaws.com',
    'alb-live-internal-1699086996.eu-central-1.elb.amazonaws.com'
]