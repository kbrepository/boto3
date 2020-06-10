## This function lists RDS instances which are not encrypted.
import boto3
import botocore.exceptions

regClient = boto3.client('ec2')
## Returns a list of regions used by AWS
region = regClient.describe_regions()
regionList = [region['RegionName'] for region in regClient.describe_regions()['Regions']]
# regionList = ['eu-west-1', 'ap-south-1']

finalDict = {}
def lambda_handler(event, context):
    for eachRegion in regionList:
        dbList = []
        rdsClient = boto3.client('rds', region_name=eachRegion)
        dbResponse = rdsClient.describe_db_instances()
        for eachDbInstance in dbResponse['DBInstances']:
            if (eachDbInstance['StorageEncrypted'] == False):
                dbInfo = {}
                try:
                    print('DB ID - {}'.format(eachDbInstance['DBInstanceIdentifier']))
                    instanceCreateTime = eachDbInstance['InstanceCreateTime']
                    dbInfo.update({ "DBInstanceIdentifier": eachDbInstance['DBInstanceIdentifier'] })
                    dbInfo.update({ "DBInstanceClass": eachDbInstance['DBInstanceClass'] })
                    dbInfo.update({ "Engine": eachDbInstance['Engine'] })
                    dbInfo.update({ "DBInstanceStatus": eachDbInstance['DBInstanceStatus'] })
                    dbInfo.update({ "MasterUsername": eachDbInstance['MasterUsername'] })
                    dbInfo.update({ "DBName": eachDbInstance['DBName'] })
                    dbInfo.update({ "Endpoint": eachDbInstance['Endpoint'] })
                    dbInfo.update({ "AllocatedStorage": eachDbInstance['AllocatedStorage'] })
                    dbInfo.update({ "InstanceCreateTime": instanceCreateTime.__str__() })
                    dbInfo.update({ "PreferredBackupWindow": eachDbInstance['PreferredBackupWindow'] })
                    dbInfo.update({ "BackupRetentionPeriod": eachDbInstance['BackupRetentionPeriod'] })
                    dbInfo.update({ "DBSecurityGroups": eachDbInstance['DBSecurityGroups'] })
                    dbInfo.update({ "VpcSecurityGroups": eachDbInstance['VpcSecurityGroups'] })
                    dbInfo.update({ "DBParameterGroups": eachDbInstance['DBParameterGroups'] })
                    dbInfo.update({ "AvailabilityZone": eachDbInstance['AvailabilityZone'] })
                    dbInfo.update({ "DBSubnetGroup": eachDbInstance['DBSubnetGroup'] })
                    dbInfo.update({ "PreferredMaintenanceWindow": eachDbInstance['PreferredMaintenanceWindow'] })
                    dbInfo.update({ "PendingModifiedValues": eachDbInstance['PendingModifiedValues'] })
                    dbInfo.update({ "MultiAZ": eachDbInstance['MultiAZ'] })
                    dbInfo.update({ "EngineVersion": eachDbInstance['EngineVersion'] })
                    dbInfo.update({ "AutoMinorVersionUpgrade": eachDbInstance['AutoMinorVersionUpgrade'] })
                    dbInfo.update({ "ReadReplicaDBInstanceIdentifiers": eachDbInstance['ReadReplicaDBInstanceIdentifiers'] })
                    dbInfo.update({ "LicenseModel": eachDbInstance['LicenseModel'] })
                    dbInfo.update({ "OptionGroupMemberships": eachDbInstance['OptionGroupMemberships'] })
                    dbInfo.update({ "PubliclyAccessible": eachDbInstance['PubliclyAccessible'] })
                    dbInfo.update({ "StorageType": eachDbInstance['StorageType'] })
                    dbInfo.update({ "DbInstancePort": eachDbInstance['DbInstancePort'] })
                    dbInfo.update({ "StorageEncrypted": eachDbInstance['StorageEncrypted'] })
                    dbInfo.update({ "DbiResourceId": eachDbInstance['DbiResourceId'] })
                    dbInfo.update({ "CACertificateIdentifier": eachDbInstance['CACertificateIdentifier'] })
                    dbInfo.update({ "DomainMemberships": eachDbInstance['DomainMemberships'] })
                    dbInfo.update({ "CopyTagsToSnapshot": eachDbInstance['CopyTagsToSnapshot'] })
                    dbInfo.update({ "MonitoringInterval": eachDbInstance['MonitoringInterval'] })
                    dbInfo.update({ "DBInstanceArn": eachDbInstance['DBInstanceArn'] })
                    dbInfo.update({ "IAMDatabaseAuthenticationEnabled": eachDbInstance['IAMDatabaseAuthenticationEnabled'] })
                    dbInfo.update({ "PerformanceInsightsEnabled": eachDbInstance['PerformanceInsightsEnabled'] })
                    dbInfo.update({ "DeletionProtection": eachDbInstance['DeletionProtection'] })
                    dbInfo.update({ "AssociatedRoles": eachDbInstance['AssociatedRoles'] })
                except rdsClient.exceptions.DBInstanceNotFoundFault as e:
                    print(e)
                
                if dbInfo:
                    dbList.append(dbInfo)
        finalDict.update({ eachRegion: dbList })
    return finalDict