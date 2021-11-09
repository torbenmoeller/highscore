import boto3
from config import config

dynamodb_client = boto3.client(
    'dynamodb',
    aws_access_key_id=config.aws_access_key_id,
    aws_secret_access_key=config.aws_secret_access_key,
    region_name=config.region_name,
    endpoint_url=config.endpoint_url)
