import sys
import VPC
import IAM
import Ec2 
import Rds
import S3
import Cloudtrail
import CDN
import CloudWatch

awsData = {}

def lambda_handler(event, context):
    awsData.clear()
    region= event['Region']
    resource = event['Resource']

    # region=str(sys.argv[1])
    # resource =str(sys.argv[2])
    if resource == 'Ec2':
        ec2Report = Ec2.ec2Audit(region)
        awsData['ec2Report']=ec2Report
        print (awsData)
    elif resource == 'IAM':
        iamReport = IAM.iamAudit()
        awsData['iamReport'] = iamReport
        iamPasswordPolicy=IAM.isStrandedPasswordPolicy()
        awsData['iamPasswordPolicy']=iamPasswordPolicy
        print (awsData)
    elif resource == 'Rds':
        rdsReport=Rds.rdsAudit(region)
        awsData['rdsReport']=rdsReport
        print (awsData)
    elif resource == 'S3':
        s3Report = S3.s3Audit()
        awsData['s3Report'] = s3Report
        print (awsData)
    elif resource == 'Cloudtrail':
        cloudtrailReport = Cloudtrail.cloudtrailAudit(region)
        awsData['cloudtrailReport'] = cloudtrailReport
    elif resource == 'CloudWatch':
        CloudwatchReport = CloudWatch.CloudWatchReport(region)
        awsData['CloudwatchReport'] = CloudwatchReport
        print (awsData)
    elif resource == 'CDN':
        CdnReport = CDN.CDNreport(region)
        awsData['CdnReport'] = CdnReport
        print (awsData)
    elif resource == 'VPC':
        VPCReport = VPC.vpcReport(region)
        awsData['VPCReport'] = VPCReport
        print (awsData)
    elif resource == 'All':
        ec2Report = Ec2.ec2Audit(region)
        awsData['ec2Report']=ec2Report
        iamReport = IAM.iamAudit()
        awsData['iamReport'] = iamReport
        iamPasswordPolicy=IAM.isStrandedPasswordPolicy()
        awsData['iamPasswordPolicy']=iamPasswordPolicy
        rdsReport=Rds.rdsAudit(region)
        awsData['rdsReport']=rdsReport
        s3Report = S3.s3Audit()
        awsData['s3Report'] = s3Report
        cloudtrailReport = Cloudtrail.cloudtrailAudit(region)
        awsData['cloudtrailReport'] = cloudtrailReport
        CloudwatchReport = CloudWatch.CloudWatchReport(region)
        awsData['CloudwatchReport'] = CloudwatchReport
        CdnReport = CDN.CDNreport(region)
        awsData['CdnReport'] = CdnReport
        VPCReport = VPC.vpcReport(region)
        awsData['VPCReport'] = VPCReport
        print (awsData)
    else:
        print ("Sorry, we don't have this resource")

    return awsData
