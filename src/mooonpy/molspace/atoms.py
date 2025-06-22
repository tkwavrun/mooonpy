# -*- coding: utf-8 -*-
"""
This module provides a class to organize atoms information
"""
from .box import Box


class AtomStyles:
    def __init__(self):
        self.style = {}


class Atoms(dict):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.box: Box = Box()
        self.style: str = ''
        self.styles = {'full': ['ID', 'molid', 'Type', 'q', 'x', 'y', 'z', 'ix', 'iy', 'iz'],
                       'full-noimage': ['ID', 'molid', 'Type', 'q', 'x', 'y', 'z'],
                       'lmpmol':['ID', 'Type', 'q', 'x', 'y', 'z'],
                       'charge': ['ID', 'Type', 'q', 'x', 'y', 'z', 'ix', 'iy', 'iz'],
                       'xyz': ['element', 'x', 'y', 'z'],
                       'custom': []
                       }
