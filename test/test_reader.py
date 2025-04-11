from src.reader import file_to_df
from unittest.mock import patch

def test_file_to_df_calls_for_csv():
    test_in = "s3://test_bucket/test_data/test_file.csv"
    with patch('src.reader.s3_csv_to_df', return_value=True) as patch_func:
        test_out = file_to_df(test_in)
        test_args = patch_func.call_args.args
    assert test_out
    assert test_args == ("test_bucket/test_data","test_file.csv")

def test_file_to_df_calls_for_json():
    test_in = "s3://test_bucket/test_data/test_file.json"
    with patch('src.reader.s3_json_to_df', return_value=True) as patch_func:
        test_out = file_to_df(test_in)
        test_args = patch_func.call_args.args
    assert test_out
    assert test_args == ("test_bucket/test_data","test_file.json")

def test_file_to_df_calls_for_parq():
    test_in = "s3://test_bucket/test_data/test_file.parquet"
    with patch('src.reader.s3_parq_to_df', return_value=True) as patch_func:
        test_out = file_to_df(test_in)
        test_args = patch_func.call_args.args
    assert test_out
    assert test_args == ("test_bucket/test_data","test_file.parquet")
## repeat for other filetypes