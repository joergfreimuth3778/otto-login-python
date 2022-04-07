import re

import boto3
import json
import subprocess

from otto_login import settings


class StsHandler:
    def __init__(self):
        self.sts = boto3.client('sts')

    def get_root_session(self):
        if self.check_session_token():
            root_session = self.get_profile_session(settings.root_session_profile)
        else:
            op_session = self.run_cmd(settings.op_signin)
            op_result = self.run_cmd(f"{settings.op_aws_token} {op_session}").strip()
            token = json.loads(op_result)['totp']
            credentials = self.get_root_session_token(token)['Credentials']
            root_session = self.get_credentials_session(credentials)

        return root_session, root_session.get_credentials()

    def get_root_session_token(self, mfa_token: str):
        return self.sts.get_session_token(
            SerialNumber=settings.mfa_device,
            TokenCode=str(mfa_token)
        )

    def save_sessions(self, sessions_to_save):
        content = self.get_login_session()
        for sessions_name, credentials in sessions_to_save.items():
            content += f"\n\n" \
                       f"[{self.profile_name(sessions_name)}]\n" \
                       f"region = {settings.region}\n" \
                       f"aws_access_key_id = {credentials.access_key}\n" \
                       f"aws_secret_access_key = {credentials.secret_key}\n" \
                       f"aws_session_token = {credentials.token}"

        self.write_credentials_file(content)

    @staticmethod
    def run_cmd(cmd):
        try:
            process = subprocess.run(cmd.split(),
                                     check=True,
                                     stdout=subprocess.PIPE,
                                     universal_newlines=True,
                                     stderr=subprocess.DEVNULL)
            return process.stdout
        except:
            raise

    @staticmethod
    def check_session_token():
        try:
            boto3.Session(
                profile_name=settings.root_session_profile
            ).client('sts').get_caller_identity()
            return True
        except:
            return False

    @staticmethod
    def get_profile_session(profile_name: str):
        return boto3.Session(
            profile_name=profile_name
        )

    @staticmethod
    def get_credentials_session(credentials):
        return boto3.Session(
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )

    @staticmethod
    def assume_role(session: boto3.session, account: str):
        return session.client('sts').assume_role(
            RoleArn=f'arn:aws:iam::{account}:role/{settings.role}',
            RoleSessionName='s3-sync'
        )

    @staticmethod
    def write_credentials_file(content):
        f = open(settings.credentials_file, 'w')
        f.write(content)
        f.close()

    @staticmethod
    def get_login_session():
        with open(settings.credentials_file, 'r') as content_file:
            content = content_file.read()

        return re.search("(\[default\]\n+aws_access_key_id.*=.+\n+aws_secret_access_key.*=.+)\n", content).group(1)

    @staticmethod
    def profile_name(env):
        if env == 'develop':
            return 'nonlive'
        return env
