import numpy as np
import pandas as pd
import re


def check_series_type(ts):
    return isinstance(ts, pd.DataFrame) or isinstance(ts, pd.Series)


def check_numeric(string):
    if re.match("^\d+?\.\d+?$", string) is None:
        return False
    return True


def check_numeric_array(array):
    for x in array:
        if not check_numeric(x):
            return False
    return True


def compute_corr(df1, df2):
    n = len(df1)
    v1, v2 = df1.values, df2.values
    sums = np.multiply.outer(v2.sum(0), v1.sum(0))
    stds = np.multiply.outer(v2.std(0), v1.std(0))

    corr = pd.DataFrame((v2.T.dot(v1) - sums / n ) / stds  / n,
                            df2.columns, df1.columns)
    corr = corr.replace([np.inf, -np.inf, np.nan], 0)

    return corr


def get_feature_type(dtypes):
    if check_series_type(dtypes):
        return 'object'

    if dtypes == 'float64' or dtypes == 'int64':
        return 'numeric'

    if dtypes == 'object':
        return 'character'


def get_decimals():
    return 4


def format_list(original_list):
    formatted_list = [round(item, get_decimals()) for item in original_list]

    return formatted_list

