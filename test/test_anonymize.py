from src.anon import anonymize
from pandas import DataFrame as df


def test_anonymize_returns_new_df():
    """
    Test that the `anonymize` function returns a new DataFrame instance
    rather than modifying the original one in-place.
    Ensures immutability is respected.
    """
    testdf = df(data={"test": range(1, 6)})
    test_out = anonymize(["test"], testdf)

    assert isinstance(test_out, df)
    assert testdf is not test_out


def test_anonymize_replaces_values():
    """
    Test that the `anonymize` function replaces all values
    in specified PII columns with obfuscated values ('***').
    Verifies that the output matches the expected obfuscated DataFrame.
    """
    testdf_in = df(data={"test": range(1, 6)})
    test_out = anonymize(["test"], testdf_in)
    testdf_expected = df(data={"test": ["***" for x in range(1, 6)]})

    assert testdf_expected.equals(test_out)


def test_anonymize_ignores_safe_values():
    """
    Test that non-PII columns remain unchanged after anonymization.
    Ensures that the function only modifies specified columns
    and leaves others intact.
    """
    fill = range(1, 6)
    testdf_in = df(data={"test": fill, "ignore": ["safe" for x in fill]})
    test_out = anonymize(["test"], testdf_in)

    testdf_expected = df(
        data={"test": ["***" for x in fill], "ignore": ["safe" for x in fill]}
    )

    assert testdf_expected.equals(test_out)
