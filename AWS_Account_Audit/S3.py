import boto3
import logging
import sys
import json
from botocore.config import Config
config = Config( read_timeout=60, retries={'max_attempts': 0})

S3Report = []
def s3Audit():
    S3Report.clear()
    S3Client = boto3.client('s3',region_name='us-east-1')
    s3_info = S3Client.list_buckets()
    for i in range(len(s3_info['Buckets'])):
        temp_info={}
        temp_info['BucketName']= s3_info['Buckets'][i]['Name']
        try :
            r_encrypt = S3Client.get_bucket_encryption(Bucket=b_name)
            temp_info['EncryptionEnabled']= "True"
        except:
            temp_info['EncryptionEnabled']= "False"
            err= ""
            for e in sys.exc_info():
                err += str(e)
            # print err
        
       
        
        S3Report.append(temp_info)
    # print (S3Report)
    return S3Report
# def lambda_handler(event, context):
#     # s3Audit()
#     s3Report = json.dumps(s3Audit())
#     print (s3Report)
#     return s3Report
