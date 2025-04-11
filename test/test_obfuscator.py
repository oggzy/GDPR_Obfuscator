from src.obfuscator import obfuscate
from pandas import DataFrame as df

def test_obfuscate_returns_new_df():
    testdf = df(data={"test":range(1, 6)})
    test_out = obfuscate(["test"],testdf)
    assert isinstance(test_out, df)
    assert testdf is not test_out

def test_obfuscate_replaces_values():
    testdf_in = df(data={"test":range(1, 6)})
    test_out=obfuscate(["test"],testdf_in)
    testdf_expected = df(data= {"test": ["***" for x in range(1,6)]})
    assert testdf_expected.equals(test_out)

def test_obfuscate_ignores_safe_values():
    fill = range(1, 6)
    testdf_in = df(data={"test": fill, "ignore" : ["safe" for x in fill]})
    test_out=obfuscate(["test"],testdf_in)
    testdf_expected = df(data= {"test": ["***" for x in fill], "ignore" : ["safe" for x in fill]})
    assert testdf_expected.equals(test_out)