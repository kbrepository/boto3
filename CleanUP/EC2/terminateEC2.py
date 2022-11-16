## This function removes EC2 instances with specific tags
import boto3
client = boto3.client('ec2')
custom_filter=Filters=[{'Name': 'tag:Name','Values': ['test',]},]
def lambda_handler(event, context):
    instance_info = client.describe_instances(Filters=custom_filter).get('Reservations',[])
    for instance_list in instance_info:
        for instance in instance_list['Instances']:
            print('Terminating instance - {}'.format(instance['InstanceId']))
            ## Terminate Instance
            terminateInstance(instance['InstanceId'])
            
def terminateInstance(instanceid):
    removeInstance=client.terminate_instances(InstanceIds=[instanceid],DryRun=False)
    print(removeInstance)
