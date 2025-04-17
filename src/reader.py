import awswrangler

def file_to_df(file_loc, file_type):
    if file_type == "csv":
        file_data = awswrangler.s3.read_csv(file_loc)
    elif file_type == "json":
        file_data = awswrangler.s3.read_json(file_loc)
    elif file_type == "parquet":
        file_data = awswrangler.s3.read_parquet(file_loc)
    else:
        raise InvalidFileType
    return file_data

class InvalidFileType(Exception):
    "File Type not supported, Obfuscate only supports csv, JSON, Parquet"
    pass