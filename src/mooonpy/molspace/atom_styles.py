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
    def __init__(self, astyles):
        
        # Set up supported styles for LAMMPS and other file formats (NOTE: for the LAMMPS 'type' attributes they can be an
        # int or str due to type labels in a LAMMPS datafile or LAMMPS molecule file - so need to use int_str function).        
        self.read = {}     # {'style' : (int or float or str)}     -> (int or float or str) sets how to read string
        self.styles = {}   # {'style' : (attr1, attr2, ...) }      -> (attr1, attr2, ...) sets attr name (e.g. 'id' 'x')
        self.defaults = {} # {'style'}: (default1, default2, ...)} -> (default1, default2, ...) sets default value for each attr
        
        self.read['angle']             = (int,  int,     int_str, float, float, float, int,  int,  int)
        self.styles['angle']           = ('id', 'molid', 'type',  'x',   'y',   'z',   'ix', 'iy', 'iz')
        self.defaults['angle']         = ( 0,    0,       0,      0.0,   0.0,   0.0,    0,    0,    0)
        
        self.read['atomic']            = (int,  int_str, float, float, float, int,  int,  int)
        self.styles['atomic']          = ('id', 'type',  'x',   'y',   'z',   'ix', 'iy', 'iz')
        self.defaults['atomic']        = ( 0,    0,      0.0,   0.0,   0.0,    0,    0,    0)
        
        self.read['body']              = (int,  int_str,  int,        float,  float, float, float, int,  int,  int)
        self.styles['body']            = ('id', 'type',   'bodyflag', 'mass', 'x',   'y',   'z',   'ix', 'iy', 'iz')
        self.defaults['body']          = ( 0,    0,        0,          0.0,   0.0,   0.0,   0.0,   0,    0,     0)
        
        self.read['bpm/sphere']        = (int,  int,     int_str,  float,      float,     float, float, float, int,  int,  int)
        self.styles['bpm/sphere']      = ('id', 'molid', 'type',   'diameter', 'density', 'x',   'y',   'z',   'ix', 'iy', 'iz')
        self.defaults['bpm/sphere']    = ( 0,    0,       0,        0.0,       0.0,       0.0,   0.0,   0.0,    0,    0,   0)
        
        self.read['rheo/thermal']      = (int,  int_str, int,      float, float,     float, float, float, int,  int,  int)
        self.styles['rheo/thermal']    = ('id', 'type',  'status', 'rho', 'energy',  'x',   'y',   'z',   'ix', 'iy', 'iz')
        self.defaults['rheo/thermal']  = ( 0,    0,       0,        0.0,   0.0,       0.0,   0.0,   0.0,   0,    0,    0)
        
        # self.read[
        # self.styles[
        # self.defaults[
        
        self.read['full']              = (int,  int,     int_str, float, float, float, float, int,  int,  int)
        self.styles['full']            = ('id', 'molid', 'type',  'q',   'x',   'y',   'z',   'ix', 'iy', 'iz')
        self.defaults['full']          = ( 0,    0,       0,      0.0,   0.0,   0.0,   0.0,   0,    0,    0)
        
        self.read['charge']            = (int,  int_str, float, float, float, float, int,  int,  int)
        self.styles['charge']          = ('id', 'type',  'q',   'x',   'y',   'z',   'ix', 'iy', 'iz')
        self.defaults['charge']        = ( 0,    0,      0.0,   0.0,   0.0,   0.0,   0.0,   0,    0)
        
        self.read['_random']           = (str,       str,       str,    int,  int,  int)
        self.styles['_random']         = ('comment', 'element', 'name', 'vx', 'vy', 'vz')
        self.defaults['_random']       = ('',        '',        '',      0,    0,    0)
        
        self.read['custom']            = ()
        self.styles['custom']          = ()
        self.defaults['custom']        = ()
        
        
        # Setup which styles should be built when an atom is generated
        if isinstance(astyles, (tuple, list)):
            build = tuple(astyles)
        else:
            build = tuple([astyles])

        
        # Consolidate all attrs and defaults into a dict and tuple to 
        # be able to initialize an Atom() object as quickly as possible
        self.all_defaults = {} # {'attr-name':default-value}
        #print('Generating atom styles: ')
        for style in self.styles:
            if style in build or 'all' in build or style.startswith('_'):
                #print(' - Building atom style: ', style)
                attrs = self.styles[style]
                defaults = self.defaults[style]
                for attr, default in zip(attrs, defaults):
                    self.all_defaults[attr] = default
        self.all_per_atom = tuple(self.all_defaults.keys())
        
        
        # Generate an Atom class with necessary slots and defaults, which will
        # be used by atom_factory() method to generate an instance of this class
        class_name = 'Atom'
        slots = self.all_per_atom
        defaults = self.all_defaults
        self.Atom = make_class(class_name, slots, defaults=defaults)

        
    def update_build(self, astyles):
        # Update defaults
        for style in astyles:
            attrs = self.styles[style]
            defaults = self.defaults[style]
            for attr, default in zip(attrs, defaults):
                self.all_defaults[attr] = default
        self.all_per_atom = tuple(self.all_defaults.keys())
        
        # Re-generate the Atom class with the new defaults
        class_name = 'Atom'
        slots = self.all_per_atom
        defaults = self.all_defaults
        self.Atom = make_class(class_name, slots, defaults=defaults)
        return
        
    def atom_factory(self):
        return self.Atom()
    
    def fill_atom(self, atom, style, data_lst):
        reader = self.read[style]
        attrs = self.styles[style]
        for string, attr, func in zip(data_lst, attrs, reader):
            value = func(string)
            setattr(atom, attr, value)
        return atom
    
    def read_full1(self, atom, style, data_lst):
        atom.id = int(data_lst[0])
        atom.molid = int(data_lst[1])
        atom.type = int(data_lst[2])
        atom.q = float(data_lst[3])
        atom.x = float(data_lst[4])
        atom.y = float(data_lst[5])
        atom.z = float(data_lst[6])
        atom.ix = int(data_lst[7])
        atom.iy = int(data_lst[8])
        atom.iz = int(data_lst[9])
        return atom