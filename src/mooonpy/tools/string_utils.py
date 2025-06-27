# -*- coding: utf-8 -*-
import re
from typing import Union


def is_float(string: str) -> bool:
    """
    regex to check if a string is a float
    """
    float_re = re.compile(r'^-?\d+(\.\d+)?([eE][-+]?\d+)?$')
    return bool(float_re.match(string))

def string2digit(string: str) -> Union[int, str, float]:
    """
    Converts a string to float or int
    :param string: String to be converted
    :type string: str
    :return: int or float or sring

    :Example:
        >>> from mooonpy.tools import string2digit
        >>> print(string2digit('5'))
        5
        >>> print(string2digit('5.1'))
        5.1
        >>> print(string2digit('5a'))
        '5a'
    """
    if string.isnumeric():
        return int(string)
    elif is_float(string):
        return float(string)
    else:
        return string