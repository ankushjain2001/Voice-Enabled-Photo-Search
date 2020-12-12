import json
import boto3
from botocore.vendored import requests
import time

#s3 = boto3.resource("s3")

host =  "https://search-cloudformation-photos-aeezsfy4tsezgwwo6rt6ouzbpq.us-east-1.es.amazonaws.com"

index = 'photos'
type = 'photo'
url = host + '/' + index + '/' + type + '/'

def detect_labels(photo, bucket):
    print("inside detect_labels", photo, bucket)
    client=boto3.client('rekognition', 'us-east-1')
    print("sending request to rekognition")
    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}}, MaxLabels=10)   
    print("after rekognition")
    print('Detected labels for ', response) 
    # print()  
    labels = []
    for label in response['Labels']:
        labels.append(label['Name'])
        
    format = {'objectKey': photo,'bucket':bucket,'createdTimestamp':time.time(),'labels':labels}
    print("sending post request to Elastic search", format)
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, data=json.dumps(format).encode("utf-8"), headers=headers)
    print("Post request sent", r.text)
    # return len(response['Labels'])


def lambda_handler(event, context):
    # TODO implement
    print("inside index-lambda!!")
    s3_info = event['Records'][0]['s3']
    bucket_name = s3_info['bucket']['name']
    key_name = s3_info['object']['key']
    
    result = detect_labels(key_name, bucket_name)
    
 
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    
    
   
