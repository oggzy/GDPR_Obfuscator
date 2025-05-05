from src.writer import df_to_bytes
import pandas as pd
from pandas import DataFrame as df

from io import BytesIO
from moto import mock_aws
from moto.core import patch_client
import pytest
import os
import boto3


@pytest.fixture(scope="function")
def aws_credentials():
    """
    Set up mocked AWS credentials for use in tests that require AWS services.
    These credentials prevent accidental use of real AWS accounts.
    """
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"


@pytest.fixture(scope="function")
def s3(aws_credentials):
    """
    Provides a mocked S3 client using Moto for use in S3-related tests.
    Ensures test isolation and no interaction with real S3.
    """
    with mock_aws():
        yield boto3.client("s3", region_name="eu-west-1")


def test_writer_writes_to_bytes_of_csv():
    """
    Test that df_to_bytes correctly converts a DataFrame
    to CSV format as bytes. Verifies output is of type `bytes`.
    """
    test_data = df({"TestA": ["test1", "test_2"],
                    "TestB": ["test1", "test_2"]})
    test_out = df_to_bytes(test_data, "csv")
    assert type(test_out) is bytes


def test_writer_writes_to_bytes_of_json():
    """
    Test that df_to_bytes correctly converts a DataFrame
    to JSON format as bytes. Verifies output is of type `bytes`.
    """
    test_data = df({"TestA": ["test1", "test_2"],
                    "TestB": ["test1", "test_2"]})
    test_out = df_to_bytes(test_data, "json")
    assert type(test_out) is bytes


def test_writer_writes_to_bytes_of_parquet():
    """
    Test that df_to_bytes correctly converts a DataFrame to Parquet format.
    """
    test_data = df({"TestA": ["test1", "test_2"],
                    "TestB": ["test1", "test_2"]})
    test_out = df_to_bytes(test_data, "parquet")
    test_file = BytesIO(test_out)

    assert type(test_out) is bytes
    assert pd.read_parquet(test_file).equals(test_data)


def test_writer_outputs_can_put_to_bucket(s3):
    """
    End-to-end test that converted byte outputs for CSV, JSON, and Parquet
    can be successfully uploaded to a mocked S3 bucket.
    Verifies that all objects are present in the bucket afterward.
    """
    patch_client(s3)
    s3.create_bucket(
        Bucket="test_bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-1"},
    )

    test_data = df({"TestA": ["test1", "test_2"],
                    "TestB": ["test1", "test_2"]})
    test_csv = df_to_bytes(test_data, "csv")
    test_json = df_to_bytes(test_data, "json")
    test_parq = df_to_bytes(test_data, "parquet")

    s3.put_object(Body=test_csv,
                  Bucket="test_bucket",
                  Key="test_csv.csv")
    s3.put_object(Body=test_json,
                  Bucket="test_bucket",
                  Key="test_json.json")
    s3.put_object(Body=test_parq,
                  Bucket="test_bucket",
                  Key="test_parquet.parquet")

    bucket_contents = s3.list_objects_v2(Bucket="test_bucket")["Contents"]

    assert len(bucket_contents) == len(
        ["test_csv.csv", "test_json.json", "test_parquet.parquet"]
    )
