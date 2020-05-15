import boto3

# for eachRegion in regionList:
#     print('Region : {}\n'.format(eachRegion))
# region = 'ap-southeast-1'

def CloudWatchReport(region):
    client = boto3.client('cloudwatch')
    response = client.describe_alarms()

    # print(response)
    tempInfo = []
    for alarms in response['MetricAlarms']:
        alarm_details={}
        # print('Metric Name : {},\nAlarm Arn :{},\nActionsEnabled :{}\n'.format(alarms['MetricName'], alarms['AlarmArn'], alarms['ActionsEnabled']))
        alarm_details['MetricName']=alarms['MetricName']
        alarm_details['AlarmArn']=alarms['AlarmArn']
        alarm_details['ActionsEnabled']=alarms['ActionsEnabled']
        
        tempInfo.append(alarm_details)
    return tempInfo
    
# CloudWatchReport(region)   