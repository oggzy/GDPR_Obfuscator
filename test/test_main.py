from src.main import GDPR_obfuscate
from pandas import DataFrame as df
from unittest.mock import patch
from moto import mock_aws
from moto.core import patch_client
import pytest
import os
import boto3

@pytest.fixture(scope='function')
def aws_credentials():

    """Mocked AWS Credentials for moto."""

    os.environ['AWS_ACCESS_KEY_ID'] = 'test'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
    os.environ['AWS_SECURITY_TOKEN'] = 'test'
    os.environ['AWS_SESSION_TOKEN'] = 'test'
    os.environ['AWS_DEFAULT_REGION'] = 'eu-west-1'


@pytest.fixture(scope='function')
def s3(aws_credentials):
    with mock_aws():
        yield boto3.client('s3', region_name='eu-west-1')

def test_obfuscate_calls_funcs():
    test_in = """{"file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv",
    "pii_fields": ["name", "email_address"]}"""
    with (patch('src.main.file_to_df', return_value="read") as patch_read,
          patch('src.main.obfuscate', return_value="obfs") as patch_obfs,
          patch('src.main.df_to_bytes', return_value="byte") as patch_byte):
        test_out = GDPR_obfuscate(test_in)
        test_args = []
        test_args.append(patch_read.call_args.args)
        test_args.append(patch_obfs.call_args.args)
        test_args.append(patch_byte.call_args.args)
    assert test_out == "byte"
    assert test_args == [("s3://my_ingestion_bucket/new_data/file1.csv","csv"),(["name", "email_address"],"read"),("obfs","csv")]

def test_obfuscates_files_in_s3_putable_format(s3):
    patch_client(s3)
    s3.create_bucket(
        Bucket='test_bucket',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'}
    )
    with open("test_csv.csv","r") as file:
      content=file.read()
      s3.put_object(Body=content, Bucket="test_bucket", Key="test_data/test_csv.csv")

    test_in = """{"file_to_obfuscate": "s3://test_bucket/test_data/test_csv.csv",
    "pii_fields": ["name", "email_address"]}"""

    test_out = GDPR_obfuscate(test_in)
    s3.put_object(Body=test_out, Bucket="test_bucket", Key="test_data/obfuscated_test_csv.csv")
    s3_out = s3.get_object(Bucket="test_bucket",Key="test_data/obfuscated_test_csv.csv")
    csv_out = s3_out["Body"].read().decode('UTF-8')
    assert csv_out == """student_id,name,course,cohort,graduation_date,email_address\n1234,***,'Software','SE-11','2024-03-31',***\n"""




