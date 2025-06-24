# -*- coding: utf-8 -*-
import importlib

__all__ = ['read_lmp_data',
           'read_lmp'
]

for name in __all__:
    module = importlib.import_module(f'.{name}', __package__)
    globals()[name] = module