import boto3, json
import time,datetime
import botocore
from datetime import datetime
from botocore.exceptions import ClientError
Iamclient = boto3.client('iam')

iamReport = []
def iamAudit():
    iamReport.clear()
    users = Iamclient.list_users()
    
    # print users
    for eachUser in users['Users']:
        temp_info = {}
        try:
            login_info = Iamclient.get_login_profile(UserName=eachUser['UserName'])
            temp_info['UserDisable'] = 'False'
        except:
            temp_info['UserDisable']= "True"
        mfa_info = Iamclient.list_mfa_devices(UserName=eachUser['UserName'])
        temp_info['UserName']=eachUser['UserName']
        if mfa_info['MFADevices'] != []:
            temp_info['MFAEnabled'] = 'True'
        else:
            temp_info['MFAEnabled'] = 'False'
        
        try:
            lastusedDate = eachUser['PasswordLastUsed'].date()
            # print(type(lastusedDate))
            # temp_info['PasswordLastUsed']=eachUser['PasswordLastUsed'].date()
            # json.dumps(lastusedDate)
            temp_info['PasswordLastUsed']=str(lastusedDate)
            print(lastusedDate)
        except KeyError:
            temp_info['PasswordLastUsed']= 'NotUsingPassword'
        # # temp_info['CreateDate']=eachUser['CreateDate'].date()
        
        accesskey_info = Iamclient.list_access_keys(UserName=eachUser['UserName'])
        # print(accesskey_info)
        for key in accesskey_info['AccessKeyMetadata']:
            if key['Status'] == 'Active':
                # print('yes')
                temp_info['KeyStatus']=key['Status']
                accesskeydate = key['CreateDate'].date()
                currentdate = datetime.now().date()
                print(accesskeydate)
                print(currentdate)
                
                diff = (currentdate - accesskeydate)
                active_day = int(diff.total_seconds()/60/60/24)
                print(active_day)

                temp_info['Active_days']=active_day
            # elif key['Status'] is None :
            #     print('No access keys used')
            #     temp_info['KeyStatus']='None'
            else:
                temp_info['KeyStatus']='Inactive'
                print('No')
                
        iamReport.append(temp_info)
    
    return iamReport
    print(iamReport)

iamPasswordPolicy = []
def isStrandedPasswordPolicy():
    iamPasswordPolicy.clear()
    get_password_policy = None
    try:
        get_password_policy = Iamclient.get_account_password_policy()
        print(get_password_policy)
    except Iamclient.exceptions.NoSuchEntityException:
        print('Please setup account password policy')


    # print("something")
    # PasswordPolicy=get_password_policy['PasswordPolicy']
    # print (PasswordPolicy)
    # correct =0
    # makechange =0
    # temp_info= {}
    # # print 
    # if PasswordPolicy['AllowUsersToChangePassword'] == True :
    #     correct = correct+1
    # else :
    #     print ("Allow users to change their own password")
    #     temp_info['AllowUsersToChangePassword']= PasswordPolicy['AllowUsersToChangePassword']
    #     makechange = makechange+1
    # if PasswordPolicy['RequireUppercaseCharacters'] == True :
    #     correct = correct+1
    # else :
    #     print ("Require at least one uppercase letter")
    #     temp_info['RequireUppercaseCharacters']= PasswordPolicy['RequireUppercaseCharacters']
    #     makechange =makechange+1
    # if PasswordPolicy['MinimumPasswordLength'] >= 6 and PasswordPolicy['MinimumPasswordLength'] <= 128:
    #     correct = correct+1
    # else :
    #     print ("Minimum password length should be greater than 6 and less than 128 char")
    #     temp_info['MinimumPasswordLength']='Minimum password length should be greater than 6 and less than 128 char'
    #     makechange =makechange+1
    # if PasswordPolicy['RequireNumbers'] == True:
    #     correct = correct +1
    # else :
    #     print ("Require at least one number")
    #     temp_info['RequireNumbers']= PasswordPolicy['RequireNumbers']
    #     makechange =makechange + 1
    # if PasswordPolicy['PasswordReusePrevention'] >= 1 and PasswordPolicy['PasswordReusePrevention'] <= 24:
    #     correct =correct+1
    # else :
    #     print ("Prevent password reuse")
    #     temp_info['PasswordReusePrevention']= 'Prevent password reuse'
    #     makechange =makechange+1
    # try :    
    #     if PasswordPolicy['HardExpiry'] == True:
    #         correct =correct+1
    #         print ("HardExpiry"+str(PasswordPolicy['HardExpiry']))
    #     else:
    #         print ("Password expiration requires administrator reset")
    #         temp_info['HardExpiry']= PasswordPolicy['HardExpiry']
    #         makechange =makechange+1
    # except:
    #     makechange =makechange +1
    #     print ("Password expiration requires administrator reset"
    # # try:
    # #     if PasswordPolicy['RequireSymbols'] == True:
    # #         correct =correct+1
    # #     else :
    # #         print ("Require at least one nonalphanumeric character")
    # #         temp_info['RequireSymbols']= PasswordPolicy['RequireSymbols']
    # #         makechange =makechange+1
    # # except:
    # #     makechange = makechange+1
    # #     print ("Require at least one nonalphanumeric character")

    # # try :
    # #     if PasswordPolicy['MaxPasswordAge'] >= 1 and PasswordPolicy['MaxPasswordAge'] <= 1095:
    # #         correct =correct +1 
    # #     else :
    # #         print ("maxpasswordage:- Minimum value of 1. Maximum value of 1095.")
    # #         temp_info['MaxPasswordAge']= 'maxpasswordage:- Minimum value of 1. Maximum value of 1095.'
    # #         makechange =makechange +1
    # # except:
    # #      makechange =makechange +1
    # #      print ("maxpasswordage:- Minimum value of 1. Maximum value of 1095.")
         
    # # if PasswordPolicy['ExpirePasswords'] == True:
    # #     correct = correct +1
    # # else :
    # #     print ("Enable password expiration")
    # #     temp_info['ExpirePasswords']= PasswordPolicy['ExpirePasswords']
    # print(correct)
    # print(makechange)
    # if correct == 0:
    #     temp_info['PasswordPolicyApplied']= 'False'
    # else:
    #     temp_info['PasswordPolicyApplied'] ='True'
    # iamPasswordPolicy.append(temp_info)
    # return iamPasswordPolicy
            
