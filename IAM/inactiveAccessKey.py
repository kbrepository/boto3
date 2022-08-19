### This function inactivates the access key with age older than 90 days.
import boto3
import time,datetime
from datetime import datetime
iamClient = boto3.client('iam')

keyAge = 500

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
                # print(accesskeydate)
                # print(currentdate)
                
                diff = (currentdate - accesskeydate)
                active_day = int(diff.total_seconds()/60/60/24)
                print('Key age on present Day - {}'.format(active_day))

                # userInfo['Active_days']=active_day
                # print(type(active_day))
                # userList = []
                # userInfo = {}
                ## List users whose access key is older than 90 days and inactive the access key.
                if active_day >= keyAge:
                    print('User - {} access key age is older than {}.'.format(eachUser['UserName'],keyAge))
                    print('Access Key is being made inactive.\n\n')
                    response = iamClient.update_access_key(UserName=eachUser['UserName'],AccessKeyId=key['AccessKeyId'],Status='Inactive')
                    print(response)
                else:
                    print('User - {} access key age is not older than {}.\n\n'.format(eachUser['UserName'],keyAge))
   
