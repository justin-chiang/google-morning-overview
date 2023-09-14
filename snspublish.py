import os
import boto3
from dotenv import dotenv_values

LOCAL = True

def publish(subject, message):
    arn = ''
    access_key = ''
    secret_key = ''

    if LOCAL:
        env = dotenv_values(".env")
        arn = env['ARN']
        access_key = env['ACCESS_KEY']
        secret_key = env['SECRET_ACCESS_KEY']
    else:
        arn = os.environ['ARN']
        access_key = os.environ['ACCESS_KEY']
        secret_key = os.environ['SECRET_ACCESS_KEY']

    sns_client = boto3.client(
        'sns',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name='us-west-1'
    )

    publish_response = sns_client.publish(TopicArn=arn, Message=message, Subject=subject)
    print(publish_response)