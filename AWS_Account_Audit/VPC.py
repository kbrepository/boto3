import boto3 
import json
import re
from datetime import datetime
from datetime import timedelta ,date
from operator import itemgetter


Ec2client = boto3.client('ec2')
regions = Ec2client.describe_regions().get('Regions',[] )
vpcdata = {'vpc-information':[]}

aws_subnet = []
aws_route = {}
VpcReport = []



def vpcReport(region):
    regionEc2client = boto3.client('ec2',region_name=region)
    vpcinfo = regionEc2client.describe_vpcs()
    print ("VPC Information")
    for vpc in vpcinfo['Vpcs']:
            temp_info ={}
            IGinfo = regionEc2client.describe_internet_gateways()
            temp_info['IsDefault']=vpc['IsDefault']
            temp_info['CidrBlock'] = vpc['CidrBlock']
            temp_info['VpcId'] = vpc['VpcId']
            for ig in IGinfo['InternetGateways']:
                if ig['Attachments'][0]['VpcId']== vpc['VpcId']:
                    temp_info['InternetGatewayId']=ig['InternetGatewayId']
            subnetinfo = regionEc2client.describe_subnets(Filters=[{'Name': 'vpc-id','Values': [vpc['VpcId'],]}])
            subnetinvpc = []
            for subnet in subnetinfo['Subnets']:
                subinfo= {}
                try:
                    subinfo['subnetId']=subnet['SubnetId']
                    subinfo['AvailabilityZone']=subnet['AvailabilityZone']
                    subinfo['subnetCidrBlock']=subnet['CidrBlock']
                except: 
                    print ("Error in subnet-info")
                subnetinvpc.append(subinfo)
            temp_info['SubnetInVPC'] = subnetinvpc
            routesinvpc = []
            routeTableinfo = regionEc2client.describe_route_tables(Filters=[{'Name': 'vpc-id','Values': [vpc['VpcId'],]},],)
            for routeTable in routeTableinfo['RouteTables']:
                routeinfo={}
                for route in routeTable['Associations']:
                    for r in routeTable['Routes']:
                        try:
                            if r['NetworkInterfaceId']:
                                routeinfo['RouteTableId'] = route['RouteTableId']
                                routeinfo['AttachedENI']="True"
                                routeinfo['State'] = r['State']
                                routeinfo['ENIinstanceId'] = r['InstanceId']
                            if r['GatewayId'].split("-")[0]=='igw':
                                print ("Public Route table----"+str(route['RouteTableId']))
                                routeinfo['RouteTableId'] = route['RouteTableId']
                                routeinfo['AttachedIG']="True"
                                routeinfo['State'] = r['State']
                            
                        except:
                            p = 0    
                if routeinfo :
                    routesinvpc.append(routeinfo)
            temp_info['RouteTableInVPC'] = routesinvpc

            VpcReport.append(temp_info)
    return VpcReport



