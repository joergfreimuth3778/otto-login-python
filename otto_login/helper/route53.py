import boto3


class Route53Handler:
    def __init__(self, session: boto3.Session):
        self.route53 = session.client('route53')

    def arecords(self, env):
        result = []
        for hosted_zone in self.__public_hosted_zone(env):
            result += self.__get_arecords(hosted_zone['Id'])

        return set(result)

    def __public_hosted_zone(self, env):
        hosted_zones = self.route53.list_hosted_zones()['HostedZones']
        return list(filter(lambda h: h['Name'].startswith(env), hosted_zones))

    def __get_arecords(self, hosted_zone_id):
        records = self.route53.list_resource_record_sets(
            HostedZoneId=hosted_zone_id
        )['ResourceRecordSets']

        return [r['Name'] for r in records]
