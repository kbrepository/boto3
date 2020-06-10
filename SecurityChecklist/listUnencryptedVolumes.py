### This function lists volume information which are not encrypted.
import boto3

regClient = boto3.client('ec2')
## Returns a list of regions used by AWS
region = regClient.describe_regions()
regionList = [region['RegionName'] for region in regClient.describe_regions()['Regions']]
# regionList = ['eu-west-1']

finalDict = {}
def lambda_handler(event, context):
    for eachRegion in regionList:
        ## Regionwise list of volumes
        volumeList = []
        ec2Client = boto3.client('ec2', region_name=eachRegion)
        volumeResponse = ec2Client.describe_volumes()
        
        for eachVolume in volumeResponse['Volumes']:
            # print(eachVolume)
            ## Dictionary for each volume's information
            volumeInfo = {}
            # print(eachVolume['Encrypted'])
            if eachVolume['Encrypted'] != 'True':
                print(eachVolume['VolumeId'])
                createTime = eachVolume['CreateTime']
                ## Attachments variable list
                Attachments = []
                attachmentInfo = {}
                # print(eachVolume['Attachments'])
                try:
                    attachTime = eachVolume['Attachments'][0]['AttachTime']
                    attachmentInfo.update({ "AttachTime": attachTime.__str__() })
                    attachmentInfo.update({ "Device": eachVolume['Attachments'][0]['Device'] })
                    attachmentInfo.update({ "InstanceId": eachVolume['Attachments'][0]['InstanceId'] })
                    attachmentInfo.update({ "State": eachVolume['Attachments'][0]['State'] })
                    attachmentInfo.update({ "VolumeId": eachVolume['Attachments'][0]['VolumeId'] })
                    attachmentInfo.update({ "DeleteOnTermination": eachVolume['Attachments'][0]['DeleteOnTermination'] })
                except:
                    print('No attachments found for Volume - {}'.format(eachVolume['VolumeId']))
                
                if attachmentInfo:
                    Attachments.append(attachmentInfo)
                ## Volume Information
                volumeInfo.update({ "VolumeId": eachVolume['VolumeId'] })
                volumeInfo.update({ "AvailabilityZone": eachVolume['AvailabilityZone'] })
                volumeInfo.update({ "CreateTime": createTime.__str__() })
                volumeInfo.update({ "Encrypted": eachVolume['Encrypted'] })
                volumeInfo.update({ "Size": eachVolume['Size'] })
                volumeInfo.update({ "SnapshotId": eachVolume['SnapshotId'] })
                volumeInfo.update({ "State": eachVolume['State'] })
                volumeInfo.update({ "Iops": eachVolume['Iops'] })
                try:
                    volumeInfo.update({ "Tags": eachVolume['Tags'] })
                except KeyError:
                    print('No Tags for Volume - {}.'.format(eachVolume['VolumeId']))
                    volumeInfo.update({ "Tags": '' })
                volumeInfo.update({ "VolumeType": eachVolume['VolumeType'] })
                try:
                    volumeInfo.update({ "MultiAttachEnabled": eachVolume['MultiAttachEnabled'] })
                except:
                    volumeInfo.update({ "MultiAttachEnabled": '' })
                    print('MultiAttachEnabled not provisioned for Volume - {}'.format(eachVolume['VolumeId']) )
                volumeInfo.update({ "Attachments": Attachments })
                # print(volumeInfo)
            if volumeInfo:
                volumeList.append(volumeInfo)
        
        finalDict.update({ eachRegion: volumeList })
        
    return finalDict