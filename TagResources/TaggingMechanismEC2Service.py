'''
This script tags resources with a predefined set of tags.

Tagging Mechanism:
1. Retrieve resources assoicated to an EC2 instance.
2. Divide resources based on the availibility of Tags.
3. Tag resources with predefined set of tags.
'''

import boto3
import datetime
region = 'eu-west-1'
instanceList = ['i-0c2029a5569eae0d9']

client = boto3.client('ec2', region_name=region)

taggedResourceList = []
unTaggedResourceList = []


def checkTagAssociation(associatedResources):
    for eachResource in associatedResources:
        prefix = eachResource.split('-')
        # print(eachResource)
        ## Check tag for instance
        if prefix[0] == 'i':
            response = client.describe_instances(InstanceIds=[eachResource])
            for i in response['Reservations']:
                for j in i['Instances']:
                    try:
                        for tags in j['Tags']:
                        # if j['Tags']:
                            print('Tags of Instance - {}'.format(tags))
                            taggedResourceList.append(eachResource)
                    except:
                        print('No tags assoicated to instance - {}'.format(eachResource))
                        unTaggedResourceList.append(eachResource)
                        
        elif prefix[0] == 'ami':
            amiResponse = client.describe_images(ImageIds=[eachResource])
            for i in amiResponse['Images']:
                try:
                    for tags in i['Tags']:
                        print('Tags of AMI - {}'.format(tags))
                        taggedResourceList.append(eachResource)
                except:
                    print('No tags associated to AMI - {}'.format(eachResource))
                    unTaggedResourceList.append(eachResource)
                    
        elif prefix[0] == 'vpc':
            vpcResponse = client.describe_vpcs(VpcIds=[eachResource])
            for i in vpcResponse['Vpcs']:
                try:
                    for tags in i['Tags']:
                        print('Tags of VPC = {}'.format(tags))
                        taggedResourceList.append(eachResource)
                except:
                    print('No tags associated to VPC - {}'.format(eachResource))
                    unTaggedResourceList.append(eachResource)
                    
        elif prefix[0] == 'subnet':
            subnetResponse = client.describe_subnets(SubnetIds=[eachResource])
            for i in subnetResponse['Subnets']:
                try:
                    for tags in i['Tags']:
                        print('Tags of Subnet - {}'.format(tags))
                        taggedResourceList.append(eachResource)
                except:
                    print('No tags associated to Subnet - {}'.format(eachResource))
                    unTaggedResourceList.append(eachResource)
        
        elif prefix[0] == 'vol':
            volResponse = client.describe_volumes(VolumeIds=[eachResource])
            for i in volResponse['Volumes']:
                try:
                    for tags in i['Tags']:
                        print('Tags of Volume - {}'.format(tags))
                        taggedResourceList.append(eachResource)
                except:
                    print('No tags associated to Volume - {}'.format(eachResource))
                    unTaggedResourceList.append(eachResource)
        
        elif prefix[0] == 'sg':
            sgResponse = client.describe_security_groups(GroupIds=[eachResource])
            for i in sgResponse['SecurityGroups']:
                try:
                    for tags in i['Tags']:
                        print('Tags of security group - {}'.format(tags))
                        taggedResourceList.append(eachResource)
                except:
                    print('No tags associated to security group - {}'.format(eachResource))
                    unTaggedResourceList.append(eachResource)
        
        elif prefix[0] == 'eni':
            print('In this loop')
            eniResponse = client.describe_network_interfaces(NetworkInterfaceIds=[eachResource])
            for i in eniResponse['NetworkInterfaces']:
                if i['TagSet']:
                    print('Tags of Network Interface - {}'.format(tags))
                    taggedResourceList.append(eachResource)
                else:
                    print('No tags assoicated to Network Interface - {}'.format(eachResource))
                    unTaggedResourceList.append(eachResource)

        else:
            print('No resources assoicated with the instance - {}'.format(instanceId))
        
### Create tag an associate to the respective untagged resources
def tagResources(resources):
    launchDate = datetime.datetime.now()
    tagDict = {    "Environment": "Prod",    "Organization": "Trigya",    "Source": "Lambda", "LaunchDate": launchDate.__str__()}
    for eachTagKey, eachTagValue in tagDict.items():
        response = client.create_tags(Resources=resources, Tags=[{ 'Key': eachTagKey, 'Value': eachTagValue}, ])
        print(response)

### Get resources associated to the EC2 Instance
def getAssociatedResources(event, context):
    # client = boto3.client('ec2', region_name=region)
    for instanceId in instanceList:
        response = client.describe_instances(InstanceIds=[instanceId],)
        
        resourceList = []    
        for i in response['Reservations']:
            for j in i['Instances']:
                # print(j)
                resourceList.append(j['InstanceId'])
                resourceList.append(j['ImageId'])
                resourceList.append(j['VpcId'])
                resourceList.append(j['SubnetId'])
                
                ### Volume Id
                for k in j['BlockDeviceMappings']:
                    resourceList.append(k['Ebs']['VolumeId'])
                    
                ### Network Interface Id and security group Id
                for l in j['NetworkInterfaces']:
                    resourceList.append(l['Groups'][0]['GroupId'])
                    resourceList.append(l['NetworkInterfaceId'])
                
                ## Function call 
                checkTagAssociation(resourceList)
                
                print('Resources with zero tags : {}'.format(unTaggedResourceList))
                print('Tagged resources : {}'.format(list(set(taggedResourceList))))
                
                ## Call tag function to create and assign tag to untagged resources
                if unTaggedResourceList:
                    print('Tagging unTaggedResourceList Resources .....')
                    tagResources(unTaggedResourceList)
                else:
                    print('There are no resources without tags.')
        # return resourceList
