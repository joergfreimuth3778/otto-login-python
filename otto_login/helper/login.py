import boto3

from otto_login import settings


class LoginHandler:
    def __init__(self):
        self.sts = boto3.client('sts')

    def get_session_token(self, mfa_token: str):
        return self.sts.get_session_token(
            SerialNumber=settings.mfa_device,
            TokenCode=mfa_token
        )

    @staticmethod
    def check_session_token():
        try:
            boto3.Session(
                profile_name=settings.intermediate_profile
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