## This function removes IAM customer managed policies with specific substring in the Policy Name
import boto3
client = boto3.client('iam')

def lambda_handler(event, context):
    response = client.list_policies(Scope='Local',)
    for Policy in response['Policies']:
        if 'dev' in (Policy['PolicyName']):
            print('Found IAM Policy - {}'.format(Policy['PolicyName']))
            removeIamPolicy(Policy['Arn'])
            
def removeIamPolicy(policyArn):
    print(policyArn)
    response = client.delete_policy(PolicyArn=policyArn)
    print('Policy Removed')
