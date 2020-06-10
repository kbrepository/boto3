## This function lists the users whose access keys are older than 45 days
import boto3
import time,datetime
from datetime import datetime

iamClient = boto3.client('iam')
finalDict = {}
keyAge = 45

def lambda_handler(event, context):
    
    ## Get all users
    users = iamClient.list_users()
    # print(users)
    
    for eachUser in users['Users']:
        
        accessKeyInfo = iamClient.list_access_keys(UserName=eachUser['UserName'])
        # print(accessKeyInfo)
        for key in accessKeyInfo['AccessKeyMetadata']:
            if key['Status'] == 'Active':
                # print('yes')
                accesskeydate = key['CreateDate'].date()
                currentdate = datetime.now().date()
                print(accesskeydate)
                print(currentdate)
                
                diff = (currentdate - accesskeydate)
                active_day = int(diff.total_seconds()/60/60/24)
                print(active_day)

                # userInfo['Active_days']=active_day
                print(type(active_day))
                userList = []
                userInfo = {}
                ## List users whose access key is older than 45 days.
                if active_day >= keyAge:
                    createDate = key['CreateDate']
                    userInfo['Status']=key['Status']
                    userInfo['UserName']=eachUser['UserName']
                    userInfo['ActiveDays']=active_day
                    userInfo['AccessKeyId']=key['AccessKeyId']
                    userInfo['CreateDate'] = createDate.__str__()
                    
                    if userInfo:
                        userList.append(userInfo)
                    if userList:
                        finalDict.update({ eachUser['UserName']:userList })

    return finalDict
