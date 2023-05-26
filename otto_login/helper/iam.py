from otto_login import settings
from otto_login import helper_functions as helper

from otto_login.helper.sts import StsHandler


class IamHandler:
    def __init__(self, sts: StsHandler):
        self.iam = sts.get_profile_session(settings.user_session_profile).client('iam')

    def rotate_access_keys(self):
        local_access_key = self.__get_local_access_key().strip()
        if local_access_key in self.__get_user_access_keys():
            self.__delete_user_access_key(local_access_key)

            new_access_key_data = self.__create_user_access_key()

            self.__save_access_key(new_access_key_data)
        else:
            raise Exception(f"Can't find local access_key ({local_access_key}) in your AWS-Account")

    def __get_user_access_keys(self):
        keys = self.iam.list_access_keys()

        return {k['AccessKeyId'] for k in keys['AccessKeyMetadata']}

    def __create_user_access_key(self):
        return self.iam.create_access_key(
            UserName=settings.ocn_user
        )

    def __delete_user_access_key(self, key):
        print(f"  key {key} deleted")
        self.iam.delete_access_key(
            UserName=settings.ocn_user,
            AccessKeyId=key
        )

    @staticmethod
    def __save_access_key(access_key_data):
        key_id = access_key_data['AccessKey']['AccessKeyId']
        key_secret = access_key_data['AccessKey']['SecretAccessKey']

        print(f"  key {key_id} saved")

        helper.run_cmd(f"aws configure "
                       f"set aws_access_key_id {key_id} --profile default")
        helper.run_cmd(f"aws configure "
                       f"set aws_secret_access_key {key_secret} --profile default")

    @staticmethod
    def __get_local_access_key():
        return helper.run_cmd("aws configure get aws_access_key_id --profile default")
