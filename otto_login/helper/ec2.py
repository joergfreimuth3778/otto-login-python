import boto3

from otto_login import settings


class Ec2Handler:
    def __init__(self, session: boto3.client):
        self.ec2 = session.client('ec2')

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
