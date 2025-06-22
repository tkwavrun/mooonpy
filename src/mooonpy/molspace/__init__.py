# -*- coding: utf-8 -*-
import importlib

__all__ = ['atoms',
           'box',
           'doc_examples',
           'graph_theory',
           'hw',
           'hw_2',
           'lmp_styles',
           'mc',
           'molspace',
]

for name in __all__:
    module = importlib.import_module(f'.{name}', __package__)
    globals()[name] = module