# import requests
import json
import pandas as pd
import xlrd
import boto3
import six

s3_client = boto3.client('s3')

def lambda_handler(event, context):
	s3 = boto3.client('s3')
	
	print(event)
	if event:
		file_obj = event["Records"][0]
		bucketname = str(file_obj['s3']['bucket']['name'])
		filename = str(file_obj['s3']['object']['key'])
		print(filename)
		print(bucketname)
		obj = s3.get_object(Bucket=bucketname, Key=filename)
		excel_df = pd.read_excel(six.BytesIO(obj['Body'].read()), encoding='utf-8')
		csv_buf = six.StringIO()
		excel_df.to_csv(csv_buf, header=True, index=False)
		csv_buf.seek(0)
		s3.put_object(Bucket=bucketname, Body=csv_buf.getvalue(), Key= 'outputs/'+filename[:-5]+'/'+filename[:-5]+'.csv')	
	return {
	"statusCode": 'It Works'
	}
	
def main():
	test_s3_event={
	  "Records": [
	    {
	      "eventVersion": "2.0",
	      "eventSource": "aws:s3",
	      "awsRegion": "us-east-1",
	      "eventTime": "1970-01-01T00:00:00.000Z",
	      "eventName": "ObjectCreated:Put",
	      "userIdentity": {
	        "principalId": "EXAMPLE"
	      },
	      "requestParameters": {
	        "sourceIPAddress": "127.0.0.1"
	      },
	      "responseElements": {
	        "x-amz-request-id": "EXAMPLE123456789",
	        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
	      },
	      "s3": {
	        "s3SchemaVersion": "1.0",
	        "configurationId": "testConfigRule",
	        "bucket": {
	          "name": "niehs-excel-conversion",
	          "ownerIdentity": {
	            "principalId": "EXAMPLE"
	          },
	          "arn": "arn:aws:s3:::example-bucket"
	        },
	        "object": {
	          "key": "toxicology.xls",
	          "size": 1024,
	          "eTag": "0123456789abcdef0123456789abcdef",
	          "sequencer": "0A1B2C3D4E5F678901"
	        }
	      }
	    }
	  ]
}
	lambda_handler(test_s3_event,'')
	
	
	
if __name__ == "__main__": 
	main() 

