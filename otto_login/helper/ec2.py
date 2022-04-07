import boto3
from requests import get

from otto_login import settings


class Ec2Handler:
    def __init__(self, session: boto3.session, env: str):
        self.ec2 = session.client('ec2')
        self.env = env

    def find_instances_by_service_tag(self, tag_value):
        return self.ec2.describe_instances(
            Filters=[
                {
                    'Name': 'tag:service',
                    'Values': [
                        tag_value,
                    ]
                },
            ]
        )['Reservations']

    def security_group_name(self):
        return settings.aws_internal_security_group.replace('ENV', self.env)

    def update_security_group(self):
        my_ip = get('https://api.ipify.org').content.decode('utf8')
        print(f"MyIP = {my_ip}")