# -*- coding: utf-8 -*-
"""
This module provides a class to organize atoms information
"""
from .box import Box
import re

class Atom:
    pass

class Styles:
    def __init__(self):
        # Set up supported styles for LAMMPS and other file formats
        self.lammps = {'full':         ('id', 'molid', 'type', 'q', 'x', 'y', 'z', 'ix', 'iy', 'iz'),
                       'charge':       ('id', 'type', 'q', 'x', 'y', 'z', 'ix', 'iy', 'iz'),
                       'body':         ('id', 'type', 'bodyflag', 'mass', 'x', 'y', 'z', 'ix', 'iy', 'iz'),
                       'custom':       ()}
        
        self.other = {'xyz':          ('element', 'x', 'y', 'z'),
                      'mol2':         ('ID', 'element', 'x', 'y', 'z', 'element', 'molid', 'name', 'q')}
        
        
        # Get all per-atom attributes from both lammps and other atom styles
        self.all_per_atom = set(['comment', 'vx', 'vy', 'vz']) # we will want to be able to have a comment and velocities
        for style in self.lammps:
            self.all_per_atom.update( set(self.lammps[style]) )
        for style in self.other:
            self.all_per_atom.update( set(self.other[style]) )
        


        
        
        # Generate how to read/write each per-atom attribute and set default
        # values, if they are not present during reading of a file.
        self.per_atom = {'id':           {'read':    self.read_int,
                                          'default': self.read_int(0)},
                         
                          'molid':        {'read':    self.read_int,
                                           'default': self.read_int(0)},
                         
                          'type':         {'read':    self.read_type,
                                           'default': self.read_int(0)},
                         
                          'q':            {'read':    self.read_float,
                                           'default': self.read_float(0)},
                         
                          'x':            {'read':    self.read_float,
                                           'default': self.read_float(0)},
                         
                          'y':            {'read':    self.read_float,
                                           'default': self.read_float(0)},
                         
                          'z':            {'read':    self.read_float,
                                           'default': self.read_float(0)},
                         
                          'ix':           {'read':    self.read_int,
                                           'default': self.read_int(0)},
                         
                          'iy':           {'read':    self.read_int,
                                           'default': self.read_int(0)},
                         
                          'iz':           {'read':    self.read_int,
                                           'default': self.read_int(0)},
                          
                          'vx':           {'read':    self.read_float,
                                           'default': self.read_float(0)},
                         
                          'vy':           {'read':    self.read_float,
                                           'default': self.read_float(0)},
                         
                          'vz':           {'read':    self.read_float,
                                           'default': self.read_float(0)},
                         
                         }
        
        
        # Check that eact per-atom read/writing and default exist for all_per_atom, if
        # not set the read/write to *_general (slower but at least will run) and default
        # value to zero (could be wrong, but in most cases should be a good default
        # option). In general the writer of this script should have most values accounted
        # for and this is a check, in-case of others adding styles and per_atom values to
        # avoid things breaking later-on down the line.        
        for attr in self.all_per_atom:
            if attr not in self.per_atom:
                default = 0
                self.per_atom[attr] = {'read':    self.read_general,
                                       'default': self.read_str(default)}
                # print(f'\nWARNING {__file__}')
                # print(f'is setting a general read/write and default: "{default}" for per-atom attribute: {attr}') 

    def is_float(self, char):
        float_re = re.compile(r'^-?\d+(\.\d+)?([eE][-+]?\d+)?$')
        return bool(float_re.match(char))                        

    def read_str(self, char):
        return str(char)

    def read_int(self, char):
        return int(char)
    
    def read_float(self, char):
        return float(char)
    
    def read_type(self, char):
        if str(char).isnumeric():
            return self.read_int(char)
        else:
            return self.read_str(char)
    
    def read_general(self, char):
        if str(char).isnumeric():
            return self.read_int(char)
        elif self.is_float(str(char)):
            return self.read_float(char)
        else:
            return self.read_str(char)


    def gen_line(self, atom, style):
        line = ''
        if style in self.lammps:
            order = self.lammps[style]
        elif style in self.other:
            order = self.other[style]
        else:
            raise KeyError(f'Error "{style}" not in styles.lammps or styles.other')
        
        line = []
        for attr in order:
            if hasattr(atom, attr):
                value = getattr(atom, attr)
            else:
                value = self.per_atom[attr]['default']
            line.append(value)
        return line
    
    def atom(self):
        # Precompile Atom class once (velocities and comments are
        # not in normal LAMMPS styles - so generate default values)
        class Atom:
            __slots__ = self.all_per_atom
            # def __init__(self, values):
            #     self.comment: str = ''
            #     self.vx: float = 0.0
            #     self.vy: float = 0.0
            #     self.vz: float = 0.0
        return Atom
    
    def gen_atom(self):            
        # Generate Atom object with pre-defined slots (any possible
        # attribute set in any supported style will be able to be
        # added at a later time)
        # class Atom:
        # #     __slots__ = self.all_per_atom
        # atom = Atom()
        return type('Atom', (), {'__slots__': self.all_per_atom})
    
    def fill_atom(self):
        return
    
    def atoms_full(self, line):
        atom = self.gen_atom()
        atom.id = int(line[0])
        atom.molid = int(line[1])
        atom.type = int(line[2])
        atom.q = float(line[3])
        atom.x = float(line[4])
        atom.y = float(line[5])
        atom.z = float(line[6])
        try:
            atom.ix = int(line[7])
            atom.iy = int(line[8])
            atom.iz = int(line[9])
        except:
            atom.ix = 0
            atom.iy = 0
            atom.iz = 0
        return atom
    



class Atoms(dict):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style: str = 'full' # will default to full and update when needed
        
        # Build this object with some composition
        self.box: Box = Box()
        self.styles: Styles = Styles()
        
    def gen_atom(self):            
        # Generate Atom object with pre-defined slots (any possible
        # attribute set in any supported style will be able to be
        # added at a later time)
        class Atom:
             __slots__ = self.styles.all_per_atom
        atom = Atom()
        return atom
    
        
    def gen_atom1(self, style, line=None):
        if style in self.styles.lammps:
            order = self.styles.lammps[style]
        elif style in self.styles.other:
            order = self.styles.other[style]
        else:
            raise KeyError(f'Error "{style}" not in styles.lammps or styles.other')
            
        # Generate Atom object with pre-defined slots (any possible
        # attribute set in any supported style will be able to be
        # added at a later time)
        class Atom:
            __slots__ = self.styles.all_per_atom
        atom = Atom()
        atom.comment = ''
        
        # File in atom attributes from line list
        if line is None: line = []
        nline = len(line)
        for n in range(len(order)):
            attr = order[n]
            if 0 <= n < nline:
                value = self.styles.per_atom[attr]['read'](line[n])
            else:
                value = self.styles.per_atom[attr]['default']
            setattr(atom, attr, value)
        return atom
        
    def shift(self, sx=0, sy=0, sz=0):
        return







        

