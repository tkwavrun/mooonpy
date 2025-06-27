# -*- coding: utf-8 -*-
import numpy as np
from numbers import Number
from typing import  Union
def aggregate_fun(fun_name: str, vector: Union[np.ndarray, list]) -> Number:
    """
    Apply generic aggregate functions to a vector, similar to the bottom row of a spreadsheet.
    Modes control values to be ignored in operation, by slicing the vector before the operation.

    Note that operating on an empty sclice will return a np.nan.

    **Currently supported Operators: fun_name must start with one of these substrings**
        - sum: Summation
        - avg: Arithmetic mean
        - std: Standard Deviation

    **Currently supported Modes: if fun_name ends with one of these substrings, the rule is applied**
        -0: Ignores 0's
        -None: Ignores None or nan

    :param fun_name: Selection of Function and Mode.
    :type fun_name: str
    :param vector: row or column vector to operate on.
    :type vector: list or numpy array
    :return: Result of operation.
    :rtype: Number

    :Example:
        >>> from mooonpy.tools import aggregate_fun
        >>> MyVect = [0,1,2]
        >>> avg_no0 = aggregate_fun('avg0', MyVect)
        1.5
        >>> avg_all = aggregate_fun('avg', MyVect)
        1.0

    """
    # Do sclicing for Mode rules
    if fun_name.endswith('0'):
        slice_ = np.nonzero(vector)
        if len(slice_) == 0:
            return np.nan
    elif fun_name.endswith('None'):
        slice_ = np.logical_not(np.isnan(vector))
        if len(slice_) == 0:
            return np.nan
    else:
        slice_ = True

    # Compute aggregate
    if fun_name.startswith('sum'):
        return np.sum(vector[slice_])
    elif fun_name.startswith('avg'):
        return np.mean(vector[slice_])
    elif fun_name.startswith('std'):
        return np.std(vector[slice_])
    else:
        raise Exception(f'ERROR: fun_name {fun_name} not recognized')