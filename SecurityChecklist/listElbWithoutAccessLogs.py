## This function lists Classic Load balancers whose access logs are not enabled.
import boto3
import botocore.exceptions

regClient = boto3.client('ec2')
## Returns a list of regions used by AWS
region = regClient.describe_regions()
regionList = [region['RegionName'] for region in regClient.describe_regions()['Regions']]
# regionList = ['eu-west-1', 'ap-south-1']

finalDict = {}
def lambda_handler(event, context):
    for eachRegion in regionList:
        elbList = []
        elbClient = boto3.client('elb', region_name=eachRegion)
        elbResponse = elbClient.describe_load_balancers()
        for eachElb in elbResponse['LoadBalancerDescriptions']:
            print(eachElb)
            elbInfo = {}
            ### Get Classic Load Balancer Name
            print(eachElb['LoadBalancerName'])
            attributeResponse = elbClient.describe_load_balancer_attributes(LoadBalancerName=eachElb['LoadBalancerName'])
            ## Filter load balancers whose access logs are not enabled.
            if attributeResponse['LoadBalancerAttributes']['AccessLog']['Enabled'] == False:
                createdTime = eachElb['CreatedTime']
                elbInfo.update({ "LoadBalancerName": eachElb['LoadBalancerName'] })
                elbInfo.update({ "DNSName": eachElb['DNSName'] })
                elbInfo.update({ "CanonicalHostedZoneName": eachElb['CanonicalHostedZoneName'] })
                elbInfo.update({ "CanonicalHostedZoneNameID": eachElb['CanonicalHostedZoneNameID'] })
                elbInfo.update({ "ListenerDescriptions": eachElb['ListenerDescriptions'] })
                elbInfo.update({ "Policies": eachElb['Policies'] })
                elbInfo.update({ "BackendServerDescriptions": eachElb['BackendServerDescriptions'] })
                elbInfo.update({ "AvailabilityZones": eachElb['AvailabilityZones'] })
                elbInfo.update({ "Subnets": eachElb['Subnets'] })
                elbInfo.update({ "VPCId": eachElb['VPCId'] })
                elbInfo.update({ "Instances": eachElb['Instances'] })
                elbInfo.update({ "HealthCheck": eachElb['HealthCheck'] })
                elbInfo.update({ "SourceSecurityGroup": eachElb['SourceSecurityGroup'] })
                elbInfo.update({ "SecurityGroups": eachElb['SecurityGroups'] })
                elbInfo.update({ "CreatedTime": createdTime.__str__() })
                elbInfo.update({ "Scheme": eachElb['Scheme'] })
                ### Update region wise list of load balancers
                if elbInfo:
                    elbList.append(elbInfo)
        ## Update dictionary regionwise
        finalDict.update({ eachRegion: elbList })
    return finalDict