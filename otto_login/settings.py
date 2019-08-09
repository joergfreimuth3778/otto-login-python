import os

ec_account = '027617375449'
accounts = {
    'live': 726963838652,
    'develop': 973172234831,
    'infra': 967223975844,
}
aws_user = os.environ["OCN_USER"]
mfa_device = f'arn:aws:iam::{ec_account}:mfa/{aws_user}'
intermediate_profile = 'session-token'
credentials_file = f'{os.environ["HOME"]}/.aws/credentials'
role = 'admin'
default_interface = 'en0'
citrix_client = "/Applications/Citrix\\ SSO.app/Contents/MacOS/Citrix\\ SSO"
required_tool = ('route', 'aws', 'git')

github_org = 'otto-ec'
github_team_id = 2770943
github_base = 'github.com'
github_api = f'https://api.{github_base}'
github_token = os.environ['GITHUB_TOKEN']
github_repo_prefix = 'tr_'
local_repo_path = f'{os.environ["HOME"]}/Otto/workspace/tracking'

firewall_url = 'https://fwauth.ov.otto.de'