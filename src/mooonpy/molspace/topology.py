# -*- coding: utf-8 -*-




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
        slots = ('bo', 'type', 'ordered', 'comment')
        defaults = {'bo':0.0, 'type':0, 'ordered':[], 'comment':''}
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
        slots = ('type', 'ordered', 'comment')
        defaults = {'type':0, 'ordered':[], 'comment':''}
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
        slots = ('type', 'ordered', 'comment')
        defaults = {'type':0, 'ordered':[], 'comment':''}
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
        slots = ('type', 'ordered', 'comment')
        defaults = {'type':0, 'ordered':[], 'comment':''}
        self.Improper = _make_class(class_name, slots, defaults=defaults)
        
    def improper_factory(self):
        return self.Improper()



