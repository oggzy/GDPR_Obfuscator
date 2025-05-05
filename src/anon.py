from pandas import DataFrame as df


def anonymize(pii_fields, file_df):
    # Make a copy of the original DataFrame to avoid modifying it
    obfuscated_df = file_df.copy(deep=True)

    # Drop the PII columns from the copy
    obfuscated_df = obfuscated_df.drop(columns=pii_fields)

    # Reinsert each PII column with obfuscated values ("***")
    for column in pii_fields:
        location = file_df.columns.get_loc(column)
        obfuscated_df.insert(location, column,
                             ["***" for i in range(len(file_df))])

    return obfuscated_df
