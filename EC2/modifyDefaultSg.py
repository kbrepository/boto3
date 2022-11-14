## This function will remove ingress and egress rules of default security groups from all regions.

import boto3
reg_client = boto3.client('ec2')

## Returns a list of regions used by AWS
region = reg_client.describe_regions()
regionList = [region['RegionName'] for region in reg_client.describe_regions()['Regions']]
# regionList = ['ap-south-1', 'ap-southeast-1']
# print(regionList)
finalDict = {}
def lambda_handler(event, context):
## Returns all available security groups in respective regions
    for eachRegion in regionList:
        print("\n\nRegion Name: "+eachRegion)
        sg_client = boto3.client('ec2',region_name=eachRegion)
        sg_response = sg_client.describe_security_groups()
        regionwiseSgs = []
        for each in sg_response['SecurityGroups']:
            # print(each['GroupId'], each['GroupName'])
            if each['GroupName'] == 'default':
                print("SecurityGroup ID : ",(each['GroupId']))
                print("Inbound Rules : ",each['IpPermissions'])
                print("Outbound Rules : ",each['IpPermissionsEgress'])
                regionwiseSgs.append(each['GroupId'])
                regionwiseSgs.append(each['IpPermissions'])
                regionwiseSgs.append(each['IpPermissionsEgress'])
        ### Remove network dependencies from default security groups
        ### Modify ingress and egrees of default security groups
                print(each['GroupId'])
                ec2 = boto3.resource('ec2',region_name=eachRegion)
                security_group = ec2.SecurityGroup(each['GroupId'])
                if each['IpPermissions']:
                    modifyIngress = security_group.revoke_ingress(DryRun=False,IpPermissions=each['IpPermissions'] )
                    print(modifyIngress)
                else:
                    print("Security Group does not have any inbound rules.")
                if each['IpPermissionsEgress']:
                    modifyEgress = security_group.revoke_egress(DryRun=False,IpPermissions=each['IpPermissionsEgress'] )
                    print(modifyEgress)
                else:
                    print("Security group does not have any outbound rules.")
        finalDict.update({eachRegion:regionwiseSgs})
    return finalDict
