import os
import re

import boto3

from otto_login import settings


class IamHandler:
    def __init__(self, session: boto3.client):
        self.iam = session.client('iam')

    def rotate_access_keys(self):
        local_access_key = self.__get_local_access_key()
        if local_access_key in self.__get_user_access_keys():
            self.__delete_user_access_key(local_access_key)

            new_access_key_data = self.__create_user_access_key()

            self.__save_access_key(new_access_key_data)
        else:
            print(f"Can't find local access_key ({local_access_key}) in your AWS-Account")
            exit(1)

    def __get_user_access_keys(self):
        keys = self.iam.list_access_keys()

        return {k['AccessKeyId'] for k in keys['AccessKeyMetadata']}

    def __create_user_access_key(self):
        return self.iam.create_access_key(
            UserName=settings.ocn_user
        )

    def __delete_user_access_key(self, key):
        self.iam.delete_access_key(
            UserName=settings.ocn_user,
            AccessKeyId=key
        )

    def __save_access_key(self, access_key_data):
        self.run_cmd(f"aws configure "
                     f"set aws_access_key_id {access_key_data['AccessKey']['AccessKeyId']} --profile default")

        self.run_cmd(f"aws configure "
                     f"set aws_secret_access_key {access_key_data['AccessKey']['SecretAccessKey']} --profile default")

    @staticmethod
    def __get_local_access_key():
        with open(settings.credentials_file, 'r') as file:
            data = file.read()
            return re.search("\[default\]\naws_access_key_id .*= (.+)\n", data).group(1)

    @staticmethod
    def run_cmd(cmd):
        try:
            os.system(cmd)
        except:
            raise
