# -*- coding: utf-8 -*-
"""
Created on Sat Jun 28 20:07:44 2025

@author: jdkem
"""

from mooonpy.molspace.doc_examples import add
import pytest


def test_add_basic():
    assert add(1, 2) == 3.0
    assert add(1.5, 2) == 3.5
    assert add(0.0, 0) == 0.0
    assert add(-1, -2.5) == -3.5

def test_add_type_error():
    with pytest.raises(TypeError):
        add("1", 2)
    with pytest.raises(TypeError):
        add(1, None)