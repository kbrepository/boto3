## This function will change the instance type of an EC2 instance.
## It will check whether the instance is in stopped state before changing the instance type.

import boto3, time

instanceType = 't2.micro'
region = 'eu-west-1'

def lambda_handler(event, context):
    client = boto3.client('ec2', region_name=region)
    print('\nChanging instance type...')
    ## Make sure to update the Instance ID below
    res2 = client.describe_instances(InstanceIds=['<Instance_ID>'])
    for l in res2['Reservations']:
        for m in l['Instances']:
            if (m['State']['Name'] == 'stopped'):
                print('Instance is stopped')
                server2=m['InstanceId']
                client.modify_instance_attribute(InstanceId=server2, InstanceType={'Value': instanceType})
                print(server2)
            elif (m['State']['Name'] == 'running'):
                print('Instance is running')
                server=m['InstanceId']
                client.stop_instances(InstanceIds=[m['InstanceId']], DryRun=False)
                time.sleep(60)
                client.modify_instance_attribute(InstanceId=server, InstanceType={'Value': instanceType})
                print(server)
                time.sleep(5)
            client.start_instances(InstanceIds=[m['InstanceId']], DryRun=False)
            print('Instance is running with modified instance type')
    
    
