import json
import os
import math
import dateutil.parser
import datetime
import time
import logging
import boto3
from botocore.vendored import requests

# COMMENT ADDED THROUGH PIPELINE

def lambda_handler(event, context):
    
    # Use this variable to perform search
    if 'q' in event["queryStringParameters"]:
        search_string = str(event["queryStringParameters"]['q'])
    else:
        search_string = 'ERROR: You have used wrong query param. use /search?q='
    
    # TODO implement
    
    client = boto3.client('lex-runtime')
    response = client.post_text(
        botName='PhotoAlbum',
        botAlias='Photobot',
        userId='1111',
        inputText=search_string
    )
    
    resp = client.delete_session(
    botName='PhotoAlbum',
    botAlias='Photobot',
    userId='1111'
    
    )
  
    print("Bot response : ", response)
    
    try:
        if response['slots'] != None:
            response_slots = response['slots'] 
    except:
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            'body': json.dumps({
                'search_string': search_string,
                's3_base_url': 'https://cc-hw3-photostore.s3.amazonaws.com/',
                'images': []
            })
        }
        
    
    url = 'https://search-cloudformation-photos-aeezsfy4tsezgwwo6rt6ouzbpq.us-east-1.es.amazonaws.com/photos/_search?q='
    
    labels=[]
    for slot in response_slots:
         if response_slots[slot] != None:
             labels.append(slot)
  
    print("Labels:",labels)

    resp = []
    for label in labels:
        url2 = url+label
        resp.append(requests.get(url2).json())
    print (resp)
    
    output = []
    for r in resp:
        if 'hits' in r:
             for val in r['hits']['hits']:
                key = val['_source']['objectKey']
                if key not in output:
                    output.append(key)
    
    print("Name of images:", output)
    
    # # NOTE: Don't remove the headers. This API is little different from others.
    # # Use the below dictionary to return the results.
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        'body': json.dumps({
            'search_string': search_string,
            's3_base_url': 'https://cloudformation-cc-hw3-photostore.s3.amazonaws.com/',
            'images': output
        })
    }
