## This function enables rotation of customer CMK
import boto3

reg_client = boto3.client('ec2')
## Returns a list of regions used by AWS
region = reg_client.describe_regions()
# regionList = [region['RegionName'] for region in reg_client.describe_regions()['Regions']]
regionList = ['ap-south-1']

def lambda_handler(event, context):
    ## List all instances
    for eachRegion in regionList:
        print("\n\nRegion Name: "+eachRegion)
        client = boto3.client('kms')
        response = client.list_keys()
        for eachKey in response['Keys']:
            # print(eachKey['KeyId'])
            describeEachKey=client.describe_key(KeyId=eachKey['KeyId'])
            ### Filtering Customer Managed Keys
            if (describeEachKey['KeyMetadata']['KeyManager']) == 'CUSTOMER':
                checkStatus=client.get_key_rotation_status(KeyId=eachKey['KeyId'])
                if (checkStatus['KeyRotationEnabled']) == False:
                    print('Enabling automatic rotation of key - {}'.format(eachKey['KeyId']))
                    enableKeyRotation(eachKey['KeyId'])
                else:
                    print('Key rotation is already Enabled for Key - {}'.format(eachKey['KeyId']))
    
def enableKeyRotation(key):
    client = boto3.client('kms')
    rotate=client.enable_key_rotation(KeyId=key)
    return rotate
