# GDPR_Obfuscator

A lightweight Python module for anonymizing personally identifiable information (PII) in CSV, JSON, and Parquet files stored in AWS S3.

📘 Overview

The GDPR_Obfuscator is designed to be integrated into AWS-based data ingestion workflows. It identifies and obfuscates sensitive fields in structured data files stored in S3 buckets. This ensures compliance with data privacy obligations for bulk data processing.

✅ Features

Obfuscates specified PII fields in CSV files stored in S3.

Returns an obfuscated byte stream compatible with boto3's put_object.

Modular and lightweight for AWS Lambda deployment.

Unit-tested and PEP-8 compliant.


🛠️ Installation

pip install -r requirements.txt

Or if packaging as a Lambda layer, include the AWSSDKPandas-Python313 default layer.

The tool is invoked using a JSON payload, like:

    {
        "file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv",
        "pii_fields": ["name", "email_address"]
    }

🧪 Sample Input File

    student_id,name,course,cohort,graduation_date,email_address
    1234,John Smith,Software,2024-03-31,j.smith@email.com

📤 Output (Obfuscated)

    student_id,name,course,cohort,graduation_date,email_address
    1234,***,Software,2024-03-31,***

🧩 Usage

    from GDPR_obfuscator.obfuscator import obfuscate

    result_bytes = obfuscate("""
        "file_to_obfuscate" ="s3://my_ingestion_bucket/new_data/file1.csv",
        pii_fields=["name", "email_address"]
    """)

result bytes will be the same format as the input file.

Optional: Save result back to S3 using boto3

    import boto3

    s3 = boto3.client('s3')
    s3.put_object(Bucket='my_output_bucket', Key='obfuscated/file1.csv', Body=result_bytes)


📦 File Format Support
Format	Status
CSV	✅ Supported
JSON	✅ Supported
Parquet	✅ Supported


🧪 Testing

Unit tests are located in the tests/ directory and can be run with:

pytest test

🚧 Non-Functional Requirements

Python 3.8+

PEP-8 compliant

No hardcoded AWS credentials

Compatible with AWS Lambda size/memory constraints

Security-audited using bandit
