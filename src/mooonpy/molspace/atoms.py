# -*- coding: utf-8 -*-
"""
This module provides a class to organize atoms information
"""
from .box import Box
from .atom_styles import Styles



class Atoms(dict):    
    def __init__(self, astyles, **kwargs):
        super().__init__(**kwargs)
        self.style: str = 'full' # will default to full and update when needed
        
        # Build this object with some composition
        self.box: Box = Box()
        self.styles: Styles = Styles(astyles)
        
        
    def shift(self, sx=0, sy=0, sz=0):
        return







        

