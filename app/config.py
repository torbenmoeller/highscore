import os
from dataclasses import dataclass

import yaml


@dataclass
class Config:
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str
    endpoint_url: str
    table_name: str


# read conf/configuration.yaml
with open("conf/configuration.yaml", "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as ex:
        print(ex)
        raise ex

config = Config(
    # secrets from environment variables
    aws_access_key_id=os.getenv('aws_access_key_id', 'FAKE_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('aws_secret_access_key', 'FAKE_SECRET_KEY'),

    # read configuration parameters
    region_name=config['aws']['region_name'],
    endpoint_url=config['aws']['dynamodb']['endpoint_url'],
    table_name=config['highscore']['table_name']
)
