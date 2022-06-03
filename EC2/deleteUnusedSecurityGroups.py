## This function will remove all the unused security groups from all regions.
import boto3

reg_client = boto3.client('ec2')

## Returns a list of regions used by AWS
region = reg_client.describe_regions()
regionList = [region['RegionName'] for region in reg_client.describe_regions()['Regions']]
# print(regionList)

## Returns all available security groups in respective regions

for eachRegion in regionList:
    print("\n\nRegion Name: "+eachRegion)
    sg_client = boto3.client('ec2',region_name=eachRegion)
    sg_response = sg_client.describe_security_groups()
    total_sgs =  set([ sg['GroupId'] for sg in sg_response['SecurityGroups'] ])
    no = len(total_sgs)
    print('Total sgs in region '+eachRegion+' are {}'.format(no))
    for i in total_sgs:
        try:
            print('Deleting... '+ i)
            response = sg_client.delete_security_group(GroupId=i, DryRun=False)
        except KeyError:
            print('Error deleting '+ i )
        except :
            print ('Security group '+ i + ' is being used ')
    
    # sg_response2 = sg_client.describe_security_groups()
    # total_sgs_after_cleanup =  set([ sg['GroupId'] for sg in sg_response2['SecurityGroups'] ])
    # no2 = len(total_sgs_after_cleanup)
    # print('Total sgs in region '+eachRegion+' after cleanup  are {}'.format(no2))
