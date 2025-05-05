import awswrangler


def file_to_df(file_loc, file_type):
    # Read file from S3 into a DataFrame based on the file type
    if file_type == "csv":
        file_data = awswrangler.s3.read_csv(file_loc)
    elif file_type == "json":
        file_data = awswrangler.s3.read_json(file_loc)
    elif file_type == "parquet":
        file_data = awswrangler.s3.read_parquet(file_loc)
    else:
        # Raise a custom exception for unsupported file types
        raise InvalidFileType
    return file_data


class InvalidFileType(Exception):
    # Custom exception for unsupported file formats
    "File Type not supported. Obfuscate only supports CSV, JSON, and Parquet."
    pass
