import json
import awswrangler
from src.anon import anonymize
from src.reader import file_to_df
from src.writer import df_to_bytes


def obfuscate(json_fields):
    # Parse the input JSON string into a Python dictionary
    inputted = json.loads(json_fields)

    # Extract the file location and determine file type from the extension
    file_loc = inputted["file_to_obfuscate"]
    split_file = file_loc.split(".")
    file_type = split_file[-1]

    # Read the input file into a pandas DataFrame
    file_data = file_to_df(file_loc, file_type)

    # Anonymize the specified PII fields
    obfuscated = anonymize(inputted["pii_fields"], file_data)

    # Convert the anonymized DataFrame back to bytes for output
    obfuscated_bytes = df_to_bytes(obfuscated, file_type)

    return obfuscated_bytes
