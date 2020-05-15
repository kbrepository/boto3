import boto3 
from datetime import datetime
from datetime import timedelta ,date
from operator import itemgetter
import sys

Ec2Report=[]
StartTime = date.today()- timedelta(30)
Start_Time = datetime(year=StartTime.year,month=StartTime.month,day=StartTime.day,)
EndTime = date.today()
today_with_time = datetime(year=EndTime.year, month=EndTime.month,day=EndTime.day,)



def ec2Audit(region):
	Ec2Report.clear()
	Ec2Client = boto3.client('ec2',region_name=region)
	cloudwatch = boto3.client('cloudwatch',region_name=region)
	instance_info = Ec2Client.describe_instances().get('Reservations',[])
	
	for instance_list in instance_info:
		temp_info = {}
		count = 0
		Datapoints = [] 
		for instance in instance_list['Instances']:
			if instance['State']['Name'] != 'terminated':
				temp_info['InstanceId']=instance['InstanceId']
				temp_info['DetailsMonitoring']=instance['Monitoring']['State']
				temp_info['InstanceState']=instance['State']['Name']
				temp_info['EbsOptimized']=instance['EbsOptimized']
				print (instance)
				temp_info['EbsDeleteOnTermination'] = instance['BlockDeviceMappings'][0]['Ebs']['DeleteOnTermination']
				temp_info['InstanceVpc']=instance['VpcId']
				isdefault= Ec2Client.describe_vpcs(VpcIds=[instance['VpcId'],])
				if isdefault['Vpcs'][0]['IsDefault'] == True:
					temp_info['isdefaultVpc'] = "True"
				else :
					temp_info['isdefaultVpc'] = "False"
				publicIp_list=[]
				temp_info['publicIps'] = []
				for eip in instance['NetworkInterfaces']:
					# print "---------------------------------------"+str(eip)
					try :
						for i in eip['PrivateIpAddresses']:
							# print i['Association']
							publicIp_list.append(i['Association']['PublicIp'])
							# print "------------------"+str(publicIp_list)
							temp_info['publicIps'] = publicIp_list
							# print "temp"+str(temp_info['publicIps'])
					except:
						temp_info['publicIps'] = "NO EIP"
				if instance['State']['Name'] == 'running':
					count = count +1
					cloudwatch_response = cloudwatch.get_metric_statistics(
					Namespace='AWS/EC2',
					MetricName='CPUUtilization',
					Dimensions=[
					{
						'Name': 'InstanceId',
						'Value': instance['InstanceId']
					},
					],
					StartTime=Start_Time,
					EndTime=today_with_time,
					Period=86400,
					Statistics=[
					'Average',
					],
					Unit='Percent')
					# print "---------"+str(instance['InstanceId'])
					for data in cloudwatch_response['Datapoints']:
						Datapoints.append(data['Average'])
					if len(Datapoints) != 0:	
						avg = sum(Datapoints)/len(Datapoints)
						temp_info['CPUUtilization']=avg
					
		# print temp_info
		Ec2Report.append(temp_info)
	return Ec2Report