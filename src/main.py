import json
import awswrangler
from src.obfuscator import obfuscate
from src.reader import file_to_df
from src.writer import df_to_bytes


def GDPR_obfuscate(json_fields):
    inputted = json.loads(json_fields)
    file_loc = inputted["file_to_obfuscate"]
    split_file = file_loc.split(".")
    file_type = split_file[-1]
    file_data = file_to_df(file_loc, file_type)
    obfuscated = obfuscate(inputted["pii_fields"], file_data)
    obfuscated_bytes = df_to_bytes(obfuscated, file_type)
    return obfuscated_bytes
