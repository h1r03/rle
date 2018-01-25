try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("WARNING: rle cannot accept pandas or numpy object")



def rle(x, col_encoded=None):
    """Main function for Run Length Encoding.

    Parameters
    ----------
    x: str, list, np.array, pd.Series, or pd.DataFrame with pd.DatetimeIndex as index
        input vector

    Returns
    -------
    encoded values and length

    """
    # if isinstance(x, list):
    #     return _encode(x)

    if isinstance(x, pd.DataFrame) & isinstance(x.index, pd.DatetimeIndex):
        return _ts_encode(x, col_encoded)


def _encode(input_string):
    """Compute the lengths of runs of equal values in input string.


    Parameters
    ----------
    input_string: str, pd.Series
        input strings to be encoded

    Returns
    -------
    lst: list
        the list of 2-element tuples that contains a pair of value / character and the number of occurence

    References
    -------
    .. [1] Run-length encoding in RosettaCode
    https://rosettacode.org/wiki/Run-length_encoding#Python

    """
    count = 1
    prev = ''
    lst = []
    for character in input_string:
        if character != prev:
            if prev:
                entry = (prev, count)
                lst.append(entry)
                # print lst
            count = 1
            prev = character
        else:
            count += 1
    else:
        entry = (character, count)
        lst.append(entry)
    return lst


def _ts_encode(df, col_encode):
    """Compute the length of discrete signal

    Parameters
    ----------
    df: pd.DataFrame
        input time-series signal that contains discrete observation with pd.DatetimeIndex as index

    Returns
    -------
    df_encoded: pd.DataFrame
       encoded time-series discrete signal that contains start time, end time for each discrete observation

    Examples
    -------
    >>> import rle
    >>> rng = pd.date_range('20130101', periods=9)
    >>> df = pd.DataFrame({'Variable':[1, 1, 1, 3, 3, 3, 7, 7, 7]}, index=rng)
    >>> rle.rle(df, col_encoded = "Variable")
    >>>
                      first       last
        Variable
        1        2013-01-01 2013-01-03
        3        2013-01-04 2013-01-06
        7        2013-01-07 2013-01-09


    """
    df.reset_index(inplace = True)
    df_encoded = df.pivot_table(index=col_encode, aggfunc={"index": ["first", "last"]})
    df_encoded.columns = df_encoded.columns.get_level_values(1)

    return df_encoded







