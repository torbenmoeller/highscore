import os

import yaml

# secrets from environment variables
aws_access_key_id = os.getenv('aws_access_key_id', 'FAKE_ACCESS_KEY')
aws_secret_access_key = os.getenv('aws_secret_access_key', 'FAKE_SECRET_KEY')

# read conf/configuration.yaml
with open("conf/configuration.yaml", "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as ex:
        print(ex)
        raise ex

# read configuration parameters
region_name = config['aws']['region_name']
endpoint_url = config['aws']['dynamodb']['endpoint_url']

table_name: str = config['highscore']['table_name']
