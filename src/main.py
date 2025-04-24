import json
import awswrangler


def GDPR_obfuscate(json_fields):
    inputted = json.loads(json_fields)
    file_loc = inputted["file_to_obfuscate"]
    split_file = file_loc.split(".")
    file_type = split_file[-1]
    file_data = file_to_df(file_loc,file_type)
    obfuscated = obfuscate(inputted["pii_fields"], file_data)
    obfuscated_bytes = df_to_bytes(obfuscated,file_type)
    return obfuscated_bytes

def df_to_bytes(df, file_type):
    if file_type == "csv":
        file_data = df.to_csv(index=False)
        file_data = bytes(file_data,"UTF-8")
    elif file_type == "json":
        file_data = df.to_json(orient="records")
        file_data = bytes(file_data,"UTF-8")
    elif file_type == "parquet":
        file_data = df.to_parquet(index=False)
    return file_data

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
    "File Type not supported, obfuscate only supports csv, JSON, Parquet"
    pass

def obfuscate(pii_fields,file_df):
    obfuscated_df = file_df.copy(deep=True)
    obfuscated_df = obfuscated_df.drop(columns=pii_fields)
    for column in pii_fields:
        location = file_df.columns.get_loc(column)
        obfuscated_df.insert(location, column, ["***" for i in range(len(file_df))])
    return obfuscated_df