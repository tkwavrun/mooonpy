# -*- coding: utf-8 -*-


def make_class(class_name, slots, defaults=None):
    defaults = defaults or {}
    
    class Dynamic:
        __slots__ = slots
        def __init__(self, values=None):
            values = values or {}
            merged = {**defaults, **values}
            for name in self.__slots__:
                setattr(self, name, merged.get(name))

    Dynamic.__name__ = class_name
    return Dynamic

def int_str(string):
    if string.isnumeric():
        return int(string)
    else:
        return string

class Styles:
    def __init__(self):
        # Set up supported styles for LAMMPS and other file formats (NOTE: for LAMMPS 'type' attributes
        # these can be an int or str due to type labels in a LAMMPS datafile or LAMMPS molecule file).        
        self.read = {}     # {'style' : (int or float or str)}     -> (int or float or str) sets how to read string
        self.styles = {}   # {'style' : (attr1, attr2, ...) }      -> (attr1, attr2, ...) sets attr name (e.g. 'id' 'x')
        self.defaults = {} # {'style'}: (default1, default2, ...)} -> (default1, default2, ...) sets default value for each attr
        
        self.read['angle']       = (int,  int,      int_str,    float, float, float, int,  int,  int)
        self.styles['angle']     = ('id', 'molid', 'type',      'x',   'y',   'z',   'ix', 'iy', 'iz')
        self.defaults['angle']   = ( 0,    0,       0,          0.0,   0.0,   0.0,   0,    0,    0)
        
        self.read['full']        = (int,   int,     int_str,   float, float, float, float, int, int, int)
        self.styles['full']      = ('id', 'molid', 'type',     'q',   'x',   'y',   'z',   'ix', 'iy', 'iz')
        self.defaults['full']    = ( 0,    0,       0,         0.0,    0.0,    0.0,   0.0,   0,    0,    0)
        
        self.read['_random']     = (str,       str,       str,    int,   int,   int)
        self.styles['_random']   = ('comment', 'element', 'name', 'vx', 'vy',  'vz')
        self.defaults['_random'] = ('',        '',        '',      0,    0,     0)

        
        # Consolidate all attrs and defaults into a dict and tuple to 
        # be able to initialize an Atom() object as quickly as possible
        self.all_defaults = {} # {'attr-name':default-value}
        for style in self.styles:
            attrs = self.styles[style]
            defaults = self.defaults[style]
            for attr, default in zip(attrs, defaults):
                self.all_defaults[attr] = default
        self.all_per_atom = tuple(self.all_defaults.keys())

        
    def gen_atom(self):
        class_name = 'Atom'
        slots = self.all_per_atom
        defaults = self.all_defaults
        Atom = make_class(class_name, slots, defaults=defaults)
        atom = Atom()
        return atom
        
    
    def fill_atom(self, atom, style, data_lst):
        read = self.read[style]
        order = self.styles[style]
        for string, attr, func in zip(data_lst, order, read):
            value = func(string)
            setattr(atom, attr, value)
        return

