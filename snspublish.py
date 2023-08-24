import boto3

from dotenv import dotenv_values

env = dotenv_values(".env")

def publish(subject, message):
    arn = env['ARN']
    sns_client = boto3.client(
        'sns',
        aws_access_key_id=env['ACCESS_KEY'],
        aws_secret_access_key=env['SECRET_ACCESS_KEY'],
        region_name='us-west-1'
    )

    publish_response = sns_client.publish(TopicArn=arn, Message=message, Subject=subject)
    print(publish_response)