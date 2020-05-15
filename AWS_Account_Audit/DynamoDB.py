import boto3

# ec2_client = boto3.client('ec2')
# region = ec2_client.describe_regions()
# regionList = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

# for region in regionList:
#     print('\nRegion Name : {}'.format(region))

region='eu-west-3'
def DynamoDBReport(region):
    client = boto3.client('dynamodb', region_name=region)
    # tableList = []
    response = client.list_tables()
    tableList = response['TableName']

    print(tableList)

    for eachTable in tableList:
        res = client.describe_table(TableName=str(eachTable))
        for tbl in res['Table']:
            print('Table Name : {}'.format(tbl['TableStatus']))

DynamoDBReport(region)


	# Table -> TableName
	#       -> TableArn
	#       -> SSEDescription -> status
	#       -> TableStatus
	#       -> ProvisionedThroughput
		