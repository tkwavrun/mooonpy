# -*- coding: utf-8 -*-
import importlib

__all__ = ['atoms',
           'box',
           'doc_examples',
           'graph_theory',
           'hw',
           'mc',
           'molspace',
           'force_field'
]

for name in __all__:
    module = importlib.import_module(f'.{name}', __package__)
    globals()[name] = module