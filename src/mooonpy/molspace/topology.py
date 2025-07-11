# -*- coding: utf-8 -*-

"""
..note:: the keys usef for all of these classes use the ordering rules below,
    so only 1 permutation is saved or searched for, and the original order is saved in the 'ordered' attribute,
        - Bonds: key = (id1, id2) # id1 < id2
        - Angles: key = (id1, id2, id3) # id1 < id3
        - Dihedrals: key = (id1, id2, id3, id4) # id1 < id4
        - Impropers: key = (id1, id2, id3, id4) # id1 < id3 < id4 # center atom is always id2, sort others

..TODO:: methods for safe lookup and __set__ with autocorrected order - 7-Jul-25

"""


def _make_class(class_name, slots, defaults=None):
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
        
        
class Bonds(dict):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.style: str = ''
        
        
        # Generate an Bond class with necessary slots and defaults, which will
        # be used by bond_factory() method to generate an instance of this class
        class_name = 'Bond'
        defaults = {'bo':0.0, 'type':0, 'ordered':[], 'comment':'', 'dist':None, 'vect':None}
        slots = tuple(defaults.keys())
        self.Bond = _make_class(class_name, slots, defaults=defaults)
        
    def bond_factory(self):
        return self.Bond()
    
    
class Angles(dict):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.style: str = ''
        
        # Generate an Angle class with necessary slots and defaults, which will
        # be used by angle_factory() method to generate an instance of this class
        class_name = 'Angle'
        defaults = {'type':0, 'ordered':[], 'comment':'', 'theta':None}
        slots = tuple(defaults.keys())
        self.Angle = _make_class(class_name, slots, defaults=defaults)
        
    def angle_factory(self):
        return self.Angle()


class Dihedrals(dict):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.style: str = ''
        
        # Generate an Dihedral class with necessary slots and defaults, which will
        # be used by dihedral_factory() method to generate an instance of this class
        class_name = 'Dihedral'
        defaults = {'type':0, 'ordered':[], 'comment':'', 'phi':None}
        slots = tuple(defaults.keys())
        self.Dihedral = _make_class(class_name, slots, defaults=defaults)
        
    def dihedral_factory(self):
        return self.Dihedral()


class Impropers(dict):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.style: str = ''
        
        # Generate an Improper class with necessary slots and defaults, which will
        # be used by improper_factory() method to generate an instance of this class
        class_name = 'Improper'
        defaults = {'type':0, 'ordered':[], 'comment':'', 'chi':None}
        slots = tuple(defaults.keys())
        self.Improper = _make_class(class_name, slots, defaults=defaults)
        
    def improper_factory(self):
        return self.Improper()



