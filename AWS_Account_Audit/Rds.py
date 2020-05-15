import boto3

def rdsAudit(region):
    RdsClient = boto3.client('rds',region_name=region)
    Ec2Client = boto3.client('ec2',region_name=region) 
    rds_response = RdsClient.describe_db_instances()
    RdsReport = []
    for rds in rds_response['DBInstances']:
        temp_info = {}
        try:    
            vpc_info = Ec2Client.describe_vpcs(VpcIds=[rds['DBSubnetGroup']['VpcId']])
            temp_info['DBInstanceIdentifier']=rds['DBInstanceIdentifier']
            temp_info['MultiAZ']=rds['MultiAZ']
            temp_info['StorageEncrypted']=rds['StorageEncrypted']
            temp_info['AllocatedStorage']=rds['AllocatedStorage']
            temp_info['BackupRetentionPeriod']=rds['BackupRetentionPeriod']
            temp_info['PreferredMaintenanceWindow']=rds['PreferredMaintenanceWindow']
            temp_info['PubliclyAccessible']=rds['PubliclyAccessible']
            temp_info['ReadReplicaDBInstanceIdentifiers']=rds['ReadReplicaDBInstanceIdentifiers']
            temp_info['DBInstanceStatus']=rds['DBInstanceStatus']
            temp_info['DeletionProtection']=rds['DeletionProtection']
            temp_info['Port']=rds['Endpoint']['Port']
            temp_info['EndpointAddress']=rds['Endpoint']['Address']
            temp_info['VpcId']=rds['DBSubnetGroup']['VpcId']
            if vpc_info['Vpcs'][0]['IsDefault'] == True:
                temp_info['isDefaultVpc'] = 'True'
            else:
                temp_info['isDefaultVpc'] = 'False'
        except:
            temp_info['DeletionProtection']='None'
        RdsReport.append(temp_info)
    # print(temp_info)
    return RdsReport

