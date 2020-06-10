## This function lists Application/Network Load balancers whose access logs are not enabled.
import boto3
import botocore.exceptions

regClient = boto3.client('ec2')
## Returns a list of regions used by AWS
region = regClient.describe_regions()
regionList = [region['RegionName'] for region in regClient.describe_regions()['Regions']]
# regionList = ['eu-west-1']

finalDict = {}
def lambda_handler(event, context):
    for eachRegion in regionList:
        lbList = []
        lbClient = boto3.client('elbv2', region_name=eachRegion)
        lbResponse = lbClient.describe_load_balancers()
        for eachLb in lbResponse['LoadBalancers']:
            # print(eachLb['LoadBalancerName'])
            response = lbClient.describe_load_balancer_attributes(LoadBalancerArn=eachLb['LoadBalancerArn'])
            for i in response['Attributes']:
                lbInfo = {}
                if (i['Key'] == 'access_logs.s3.enabled'):
                    if (i['Value'] == 'false' ):
                        print(eachLb['LoadBalancerArn'])
                        createdTime = eachLb['CreatedTime']
                        lbInfo.update({ "LoadBalancerArn": eachLb['LoadBalancerArn'] })
                        lbInfo.update({ "DNSName": eachLb['DNSName'] })
                        lbInfo.update({ "CanonicalHostedZoneId": eachLb['CanonicalHostedZoneId'] })
                        lbInfo.update({ "CreatedTime": createdTime.__str__() })
                        lbInfo.update({ "LoadBalancerName": eachLb['LoadBalancerName'] })
                        lbInfo.update({ "Scheme": eachLb['Scheme'] })
                        lbInfo.update({ "VpcId": eachLb['VpcId'] })
                        lbInfo.update({ "State": eachLb['State'] })
                        lbInfo.update({ "Type": eachLb['Type'] })
                        lbInfo.update({ "AvailabilityZones": eachLb['AvailabilityZones'] })
                        lbInfo.update({ "IpAddressType": eachLb['IpAddressType'] })
                        try:
                            lbInfo.update({ "SecurityGroups": eachLb['SecurityGroups'] })
                        except:
                            print('No security groups provisioned.')
                if lbInfo:
                    lbList.append(lbInfo)
        ## Update dictionary regionwise
        finalDict.update({ eachRegion: lbList })
    return finalDict