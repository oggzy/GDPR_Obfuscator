from src.writer import df_to_bytes
from pandas import DataFrame as df

def test_writer_writes_to_bytes_of_csv():
    Test_data = df({"TestA":["test1","test_2"],"TestB":["test1","test_2"]})
    test_out = df_to_bytes(Test_data, "csv")
    assert type(test_out) is bytes