from src.main import GDPR_obfuscate
from pandas import DataFrame as df
from unittest.mock import patch
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


def test_obfuscate_calls_funcs():
    """
    Test that the `GDPR_obfuscate` function correctly calls the
    necessary helper functions (`file_to_df`, `obfuscate`, `df_to_bytes`)
    with the appropriate arguments. This ensures that the process
    flow between these functions works as expected.
    """
    test_in = """{"file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv",
    "pii_fields": ["name", "email_address"]}"""

    # Mocking the helper functions
    with (
        patch("src.main.file_to_df", return_value="read") as patch_read,
        patch("src.main.obfuscate", return_value="obfs") as patch_obfs,
        patch("src.main.df_to_bytes", return_value="byte") as patch_byte,
    ):
        test_out = GDPR_obfuscate(test_in)

        # Capture the arguments passed to each mocked function
        test_args = []
        test_args.append(patch_read.call_args.args)
        test_args.append(patch_obfs.call_args.args)
        test_args.append(patch_byte.call_args.args)

    # Verify that the output of GDPR_obfuscate matches the expected byte output
    assert test_out == "byte"

    # Ensure the helper functions were called with the expected arguments
    assert test_args == [
        ("s3://my_ingestion_bucket/new_data/file1.csv", "csv"),
        (["name", "email_address"], "read"),
        ("obfs", "csv"),
    ]


def test_obfuscates_files_in_s3_putable_format(s3):
    """
    Test that the `GDPR_obfuscate` function correctly obfuscates
    a file stored in S3 and outputs the obfuscated data in a valid
    format (CSV). Verifies that the output can be uploaded to an S3
    bucket and retrieved correctly.
    """
    patch_client(s3)

    # Create a bucket in the mocked S3 environment
    s3.create_bucket(
        Bucket="test_bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-1"},
    )

    # Upload a sample CSV file to the mocked S3 bucket
    with open("test_csv.csv", "r") as file:
        content = file.read()
        s3.put_object(Body=content,
                      Bucket="test_bucket",
                      Key="test_data/test_csv.csv")

    # Input for the GDPR_obfuscate function
    test_in = """{"file_to_obfuscate": "s3://test_bucket/test_data/test_csv.csv",
    "pii_fields": ["name", "email_address"]}"""

    # Call GDPR_obfuscate to get the obfuscated data
    test_out = GDPR_obfuscate(test_in)

    # Upload the obfuscated data to S3
    s3.put_object(
        Body=test_out,
        Bucket="test_bucket",
        Key="test_data/obfuscated_test_csv.csv"
    )

    # Retrieve the obfuscated file from S3
    s3_out = s3.get_object(
        Bucket="test_bucket",
        Key="test_data/obfuscated_test_csv.csv"
    )
    csv_out = s3_out["Body"].read().decode("UTF-8")

    # Verify that the obfuscated content matches the expected result
    assert (
        csv_out ==
        "student_id,name,course,cohort,graduation_date,email_address"
        "\n1234,***,'Software','SE-11','2024-03-31',***\n"
    )
