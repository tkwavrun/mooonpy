# -*- coding: utf-8 -*-
import importlib
import os

#from .molspace.molspace import Molspace
#__all__ = ['Molspace']

__all__ = []

# Get the current directory (the package root)
_package_dir = os.path.dirname(__file__)

# List of submodules/folders to import
_submodules = ['guis', 'molspace', 'programs', 'thermospace', 'tools', 'xrdspace']

for name in _submodules:
    if os.path.isdir(os.path.join(_package_dir, name)):
        module = importlib.import_module(f'.{name}', __package__) # f'.{name}'
        #print(name, module,  __package__)
        globals()[name] = module
        __all__.append(name)