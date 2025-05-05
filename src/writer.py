def df_to_bytes(df, file_type):
    # Convert the DataFrame to the appropriate file format based on type
    if file_type == "csv":
        # Convert to CSV string without index, then encode to bytes
        file_data = df.to_csv(index=False)
        file_data = bytes(file_data, "UTF-8")
    elif file_type == "json":
        # Convert to JSON string (records format), then encode to bytes
        file_data = df.to_json(orient="records")
        file_data = bytes(file_data, "UTF-8")
    elif file_type == "parquet":
        # Convert to binary Parquet format directly (already returns bytes)
        file_data = df.to_parquet(index=False)
    return file_data
