
def file_to_df(file_loc):
    split_loc = file_loc.split("/")
    split_file = file_loc.split(".")
    if split_file[-1] == "csv":
        file_data = s3_csv_to_df(split_loc[2]+"/"+split_loc[3] , split_loc[-1])
    elif split_file[-1] == "json":
        file_data = s3_json_to_df(split_loc[2]+"/"+split_loc[3] , split_loc[-1])
    elif split_file[-1] == "parquet":
        file_data = s3_parq_to_df(split_loc[2]+"/"+split_loc[3] , split_loc[-1])

    return file_data


def s3_csv_to_df(bucket,file):
    pass

def s3_json_to_df(bucket,file):
    pass

def s3_parq_to_df(bucket,file):
    pass