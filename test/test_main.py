from src.main import GDPR_obfuscate
from unittest.mock import patch

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

