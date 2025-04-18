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