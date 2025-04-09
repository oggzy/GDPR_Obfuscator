from pandas import DataFrame as df

def obfuscate(pii_fields,file_df):
    obfuscated_df = file_df.copy(deep=True)
    obfuscated_df = obfuscated_df.drop(columns=pii_fields)
    for column in pii_fields:
        location = file_df.columns.get_loc(column)
        obfuscated_df.insert(location, column, ["***" for i in range(len(file_df))])
    return obfuscated_df
        