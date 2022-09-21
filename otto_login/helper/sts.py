import boto3
import json

from otto_login import settings
from otto_login import helper_functions as helper


class StsHandler:
    def __init__(self):
        self.sts = boto3.client('sts')

    def save_session(self, op_session):
        op_result = helper.run_cmd(f"{settings.aws_otp_token} {op_session}").strip()
        token = json.loads(op_result)['totp']
        self.save_user_session(self.get_user_session_token(token)['Credentials'])

    @staticmethod
    def check_user_session_token():
        # noinspection PyBroadException
        try:
            boto3.Session(
                profile_name=settings.user_session_profile
            ).client('sts').get_caller_identity()
            return True
        except Exception:
            return False

    @staticmethod
    def get_profile_session(profile_name: str):
        return boto3.Session(
            profile_name=profile_name
        )

    def get_user_session_token(self, mfa_token: str):
        return self.sts.get_session_token(
            SerialNumber=settings.mfa_device,
            TokenCode=str(mfa_token)
        )

    @staticmethod
    def save_user_session(credentials):
        aws_cmd = 'aws configure set'
        profile_param = f'--profile {settings.user_session_profile}'
        helper.run_cmd(f"{aws_cmd} aws_access_key_id {credentials['AccessKeyId']} {profile_param}")
        helper.run_cmd(f"{aws_cmd} aws_secret_access_key {credentials['SecretAccessKey']} {profile_param}")
        helper.run_cmd(f"{aws_cmd} aws_session_token {credentials['SessionToken']} {profile_param}")
