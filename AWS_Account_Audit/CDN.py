import boto3

# ec2_client = boto3.client('ec2')
# region = ec2_client.describe_regions()
# regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

# for eachRegion in regions:
#     print('\n'+eachRegion+'\n')

def CDNreport(region):
    client = boto3.client('cloudfront', region_name=region)
    response = client.list_distributions()

    allDistributions = []
    try:
        for items in response['DistributionList']['Items']:
            try:
                allDistributions.append(items['Id'])
            except:
                print('Error')
    except KeyError:
        print('CDN Not available.')
    #print(allDistributions)

    cdn_details = []
    for eachCDN in allDistributions:
        cdn_info = client.get_distribution(Id=eachCDN)
        distribution_details = {}
        for i in cdn_info['Distribution']['DistributionConfig']['Origins']['Items']:
            try:
                distribution_details['Id']=eachCDN
                distribution_details['ARN']=cdn_info['Distribution']['ARN']
                distribution_details['DomainName']=cdn_info['Distribution']['DomainName']
                distribution_details['Status']=cdn_info['Distribution']['Status']
                distribution_details['Comment']=cdn_info['Distribution']['DistributionConfig']['Comment']
                distribution_details['Origin']=i['DomainName']
                distribution_details['cNames']=cdn_info['Distribution']['DistributionConfig']['Aliases']['Items']
                
            except KeyError:
                distribution_details['cNames']='None'
                # print('Alias not found')
        cdn_details.append(distribution_details)
    # print(distribution_details)
    return cdn_details
# print(cdn_details)
