import boto3
import datetime
import time
from time import gmtime, strftime
today_date=int(strftime("%d",gmtime()))
date_fmt = strftime("%b %d %Y", gmtime())
region='us-west-2'

def getInstanceList(instance_response):
    instancelist=[]
    # instance_response = ec2client.describe_instances()
    for reservation in instance_response["Reservations"]:
        for i in reservation["Instances"]:
            instancelist.append(i['InstanceId'])
    return instancelist
# print(len(instancelist))

def dateCompare(imgresponse,instancelist):
    print ("In date compare")
    updated_instance_list=[]
    for img in imgresponse:
        print ("Image"+str(img))
        for j in instancelist:
            print ("j"+j+"images   "+img['Tags'][1]['Value'])
            if j==img['Tags'][1]['Value']:
                print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                c=(str(img['CreationDate']).split("T"))
                creation= datetime.datetime.strptime(c[0],'%Y-%m-%d').date()
                if deletion >=creation:
                    updated_instance_list.append(j)
                    print ("Retention period of "+j+" is completed.......")
                else:
                    print ("Retention period not completed...")
            else :
                 updated_instance_list.append(j)
    print (updated_instance_list)
    create_ami(updated_instance_list)

def create_ami(toBecreatedAmi):
    print ("Creating AMI")
    print(region)
    amiClient = boto3.client('ec2', region_name=region)
    if toBecreatedAmi:
        for eachInstance in toBecreatedAmi:
            newAMI=amiClient.create_image(Description='Created-via-lambda-service',DryRun=False, InstanceId=eachInstance, Name='Daily-Backup '+eachInstance+date_fmt, NoReboot=True)
            time.sleep(5)
            print(newAMI)
            amiTag=amiClient.create_tags(DryRun=False,Resources=[newAMI['ImageId'],],
            Tags=[{'Key': 'AMI-creation-via-Lambda','Value': 'Autocreation-AMI'},{'Key':'InstanceId','Value':eachInstance}])
        print('Ami is ready.')
    else:
        print ("No instance in the list to create AMI.")

def checkSnapshot(imgresponse,snapshots):
    for img in imgresponse:
        c=(str(img['CreationDate']).split("T"))
        creation= datetime.datetime.strptime(c[0],'%Y-%m-%d').date()
        if creation<=deletion:
            AMI_to_delete=img['ImageId']
            ec2client.deregister_image(DryRun=False,ImageId=AMI_to_delete)
            print ("Retention period of AMI is completed...deleting AMI")
            for snapshot in snapshots:
                if snapshot['Description'].find(AMI_to_delete) > 0:
                    snap = ec2client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                    print ("Retention period of snapshot is completed... deleting snapshot"+str(snap))
        else:
            print ("AMI and snapshot are not deleted ")

def lambda_handler(event, context):
	region=event['region']
	print(region)
	ec2client = boto3.client('ec2', region_name=region)
	instance_response = ec2client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped', 'running']}])
	instancelist=getInstanceList(instance_response)
	print(instancelist)
	print(len(instancelist))
	imgresponse = ec2client.describe_images(Owners=['<ACCOUNT_ID>']).get('Images',[]) # List AMI's
	print ("Image Response"+str(imgresponse))
	snapshots = ec2client.describe_snapshots(MaxResults=1000, OwnerIds=['<ACCOUNT_ID>'])['Snapshots']
	deletion=(datetime.datetime.now() - datetime.timedelta(days=3)).date()
	print(deletion)
	if imgresponse:
		print ("In imgeresponse")
		dateCompare(imgresponse,instancelist)
	else:
		print ("else imgeresponse ")
		create_ami(instancelist)
		print ("Checking Snapshot")
	snap=checkSnapshot(imgresponse,snapshots)
	print (snap)
	
