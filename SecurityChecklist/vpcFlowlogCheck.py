### This function lists those VPC's whose flow logs are not enabled.
import boto3
regClient = boto3.client('ec2')
region = regClient.describe_regions()
regionList = [region['RegionName'] for region in regClient.describe_regions()['Regions']]
# regionList = ['eu-west-1']

finalDict = {}
def lambda_handler(event, context):
    for eachRegion in regionList:
        flowLogNotEnable = []
        client = boto3.client('ec2',region_name=eachRegion)
        try :
            listVPcId = client.describe_vpcs()
            for vpclist in listVPcId['Vpcs']:
                flowlogResponse = client.describe_flow_logs(Filters=[{'Name': 'resource-id','Values': [vpclist['VpcId'],]},],)
                vpcInfo = {}
                if not flowlogResponse['FlowLogs']:
                    # print(vpclist)
                    vpcInfo.update({ "VpcId": vpclist['VpcId']})
                    vpcInfo.update({ "CidrBlock": vpclist['CidrBlock'] })
                    vpcInfo.update({ "DhcpOptionsId": vpclist['DhcpOptionsId'] })
                    vpcInfo.update({ "State": vpclist['State'] })
                    vpcInfo.update({ "OwnerId": vpclist['OwnerId'] })
                    vpcInfo.update({ "InstanceTenancy": vpclist['InstanceTenancy'] })
                    vpcInfo.update({ "CidrBlockAssociationSet": vpclist['CidrBlockAssociationSet'] })
                    vpcInfo.update({ "IsDefault": vpclist['IsDefault'] })
                    try:
                        vpcInfo.update({ "Tags": vpclist['Tags'] })
                    except:
                        print('No Tags for VPC - {}.'.format(vpclist['VpcId']))
                    
                    if vpcInfo:
                        flowLogNotEnable.append(vpcInfo)
            finalDict.update({eachRegion:flowLogNotEnable})
        except Exception as e:
            print (e)
    return finalDict