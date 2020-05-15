import boto3

CloudTrailReport = []
def cloudtrailAudit(region):
    CloudTrailReport.clear()
    multiRegionalTrail = False
    CloudtrailClient = boto3.client('cloudtrail', region_name=region)
    try:
        trail_info = CloudtrailClient.describe_trails()
        for trails in trail_info['trailList']:
            temp_info= {}
            print (trails)
            if (trails['IsMultiRegionTrail'] == True):
                regionName = 'Global'
                temp_info['S3BucketName']= trails['S3BucketName']
                temp_info['TrailARN'] =trails['TrailARN']
                temp_info['LogFileValidationEnabled'] = trails['LogFileValidationEnabled']
                temp_info['IsMultiRegionTrail']=trails['IsMultiRegionTrail']
                
                
                print("Trail name : {}, Is Trail MultiRegiobal : {} \n".format(trails['Name'], trails['S3BucketName'], trails['TrailARN'], trails['LogFileValidationEnabled'], trails['IsMultiRegionTrail']))
                multiRegionalTrail = True
                CloudTrailReport.append(temp_info)
                print(multiRegionalTrail)
            if (trails['IsMultiRegionTrail'] == False):
                temp_info['S3BucketName']= trails['S3BucketName']
                temp_info['TrailARN'] =trails['TrailARN']
                temp_info['LogFileValidationEnabled'] = trails['LogFileValidationEnabled']
                temp_info['IsMultiRegionTrail']=trails['IsMultiRegionTrail']
                print("Trail name : {}, Is Trail MultiRegiobal : {} \n".format(trails['Name'], trails['IsMultiRegionTrail']))
                print ("trail")
                CloudTrailReport.append(temp_info)
        
    except:
        temp_info = {}
        print ('CloudTrails unavailable.')
        temp_info['isCloudtrailAvailable'] = "False"
        CloudTrailReport.append(temp_info)
    print (CloudTrailReport)
    return CloudTrailReport