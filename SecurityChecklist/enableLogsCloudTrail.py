## This script will enable cloudtrail logging
import boto3
import botocore
regionClient = boto3.client('ec2')
region = regionClient.describe_regions()


for eachRegion in region['Regions']:
    trailClient = boto3.client('cloudtrail',region_name=eachRegion['RegionName'])   
    try :
        listTrail = trailClient.list_trails()
        for i in listTrail['Trails']:
            if i['HomeRegion'] == eachRegion:
                try:
                    loggingResponse = trailClient.start_logging(Name=i['Name'])
                    # print (trailname)
                    print (loggingResponse)
                except Exception as e:
                        print (e)
    except Exception as e:
        print (e)
    