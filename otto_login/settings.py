import os

ec_account = '027617375449'
accounts = {
    'live': 726963838652,
    'develop': 973172234831,
    'infra': 967223975844,
}
mfa_device = f'arn:aws:iam::{ec_account}:mfa/{os.environ["OCN_USER"]}'
intermediate_profile = 'session-token'
credentials_file = f'{os.environ["HOME"]}/.aws/credentials'
role = 'admin'
default_interface = 'en0'
