from src.reader import file_to_df
from unittest.mock import patch
from pandas import DataFrame as df
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


@pytest.fixture
def bucket(s3):
    """
    Creates a mocked S3 bucket and uploads a sample CSV file to it.
    This fixture sets up the required environment for tests
    that interact with S3.
    """
    s3.create_bucket(
        Bucket="test_bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-1"},
    )
    # Upload a sample CSV file to the mocked S3 bucket
    with open("test_csv.csv", "rb") as f:
        s3.put_object(Body=f,
                      Bucket="test_bucket",
                      Key="test_data/test_csv.csv")


def test_file_to_df_calls_for_csv():
    """
    Test that the `file_to_df` function calls `awswrangler.s3.read_csv`
    when processing a CSV file. This verifies that the correct function
    is called and that the file path is passed correctly as an argument.
    """
    test_in = "s3://test_bucket/test_data/test_file.csv"
    with patch("awswrangler.s3.read_csv", return_value=True) as patch_func:
        test_out = file_to_df(test_in, "csv")
        test_args = patch_func.call_args.args

    # Assert that the function calls return a result
    assert test_out
    # Assert that the correct arguments are passed to the read_csv function
    assert test_args[0] == test_in
    # Ensure that only one argument (the file path) is passed
    assert len(test_args) == 1


def test_file_to_df_calls_for_json():
    """
    Test that the `file_to_df` function  calls `awswrangler.s3.read_json`
    when processing a JSON file. This verifies that the correct function
    is called and that the file path is passed correctly as an argument.
    """
    test_in = "s3://test_bucket/test_data/test_file.json"
    with patch("awswrangler.s3.read_json", return_value=True) as patch_func:
        test_out = file_to_df(test_in, "json")
        test_args = patch_func.call_args.args

    # Assert that the function calls return a result
    assert test_out
    # Assert that the correct arguments are passed to the read_json function
    assert test_args[0] == test_in
    # Ensure that only one argument (the file path) is passed
    assert len(test_args) == 1


def test_file_to_df_calls_for_parq():
    """
    Test that the `file_to_df` function calls `awswrangler.s3.read_parquet`
    when processing a Parquet file. This verifies that the correct function
    is called and that the file path is passed correctly as an argument.
    """
    test_in = "s3://test_bucket/test_data/test_file.parquet"
    with patch("awswrangler.s3.read_parquet", return_value=True) as patch_func:
        test_out = file_to_df(test_in, "parquet")
        test_args = patch_func.call_args.args

    # Assert that the function calls return a result
    assert test_out
    # Assert that the correct arguments are passed to the read_parquet function
    assert test_args[0] == test_in
    # Ensure that only one argument (the file path) is passed
    assert len(test_args) == 1


def test_file_reads_from_s3(bucket, s3):
    """
    Test that the `file_to_df` function correctly reads a CSV file
    from the mocked S3 bucket and returns a DataFrame that matches
    the expected data.
    """
    patch_client(s3)

    # Call the file_to_df function to read the file from S3
    test_out = file_to_df("s3://test_bucket/test_data/test_csv.csv", "csv")

    # Define the expected DataFrame for comparison
    test_df = df(
        {
            "student_id": [1234],
            "name": ["'John Smith'"],
            "course": ["'Software'"],
            "cohort": ["'SE-11'"],
            "graduation_date": ["'2024-03-31'"],
            "email_address": ["'j.smith@email.com'"],
        }
    )

    # Assert that the output is a DataFrame
    assert isinstance(test_out, df)
    # Assert that the DataFrame matches the expected output
    assert test_out.equals(test_df)
