from src.reader import file_to_df
from unittest.mock import patch
from pandas import DataFrame as df
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


@pytest.fixture
def bucket(s3):
    s3.create_bucket(
        Bucket='test_bucket',
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'}
    )
    with open('test_csv.csv', 'rb') as f:
        s3.put_object(
                        Body=f, Bucket='test_bucket',
                        Key='test_data/test_csv.csv'
                    )

def test_file_to_df_calls_for_csv():
    test_in = "s3://test_bucket/test_data/test_file.csv"
    with patch('awswrangler.s3.read_csv', return_value=True) as patch_func:
        test_out = file_to_df(test_in,"csv")
        test_args = patch_func.call_args.args
    assert test_out
    assert test_args[0] == test_in
    assert len(test_args) == 1

def test_file_to_df_calls_for_json():
    test_in = "s3://test_bucket/test_data/test_file.json"
    with patch('awswrangler.s3.read_json', return_value=True) as patch_func:
        test_out = file_to_df(test_in,"json")
        test_args = patch_func.call_args.args
    assert test_out
    assert test_args[0] == test_in
    assert len(test_args) == 1

def test_file_to_df_calls_for_parq():
    test_in = "s3://test_bucket/test_data/test_file.parquet"
    with patch('awswrangler.s3.read_parquet', return_value=True) as patch_func:
        test_out = file_to_df(test_in,"parquet")
        test_args = patch_func.call_args.args
    assert test_out
    assert test_args[0] == test_in
    assert len(test_args) == 1

def test_file_reads_from_s3(bucket, s3):
    patch_client(s3)
    test_out = file_to_df("s3://test_bucket/test_data/test_csv.csv","csv")
    test_df = df({"student_id" : [1234],"name":["'John Smith'"],"course": ["'Software'"],"cohort": ["'SE-11'"],"graduation_date":["'2024-03-31'"],"email_address":["'j.smith@email.com'"]})
    assert isinstance(test_out, df)
    assert test_out.equals(test_df)