import awswrangler

def file_to_df(file_loc):
    split_file = file_loc.split(".")
    if split_file[-1] == "csv":
        file_data = awswrangler.s3.read_csv(file_loc)
    elif split_file[-1] == "json":
        file_data = awswrangler.s3.read_json(file_loc)
    elif split_file[-1] == "parquet":
        file_data = awswrangler.s3.read_parquet(file_loc)
    return file_data