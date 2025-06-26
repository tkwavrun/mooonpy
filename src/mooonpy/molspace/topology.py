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
        
        
class Bonds(dict):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.style: str = ''
        
        
        class_name = 'Bond'
        slots = ('bo', 'type', 'ordered', 'comment')
        defaults = {'bo':0.0, 'type':0, 'ordered':[], 'comment':''}
        self.Bond = make_class(class_name, slots, defaults=defaults)
        
    def bond_factory(self):
        # class_name = 'Bond'
        # slots = ('bo', 'type', 'ordered', 'comment')
        # defaults = {'bo':0.0, 'type':0, 'ordered':[], 'comment':''}
        # Bond = make_class(class_name, slots, defaults=defaults)
        return self.Bond()
    
    
class Angles(dict):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.style: str = ''
        
        
        class_name = 'Angle'
        slots = ('type', 'ordered', 'comment')
        defaults = {'type':0, 'ordered':[], 'comment':''}
        self.Angle = make_class(class_name, slots, defaults=defaults)
        
    def angle_factory(self):
        # class_name = 'Angle'
        # slots = ('type', 'ordered', 'comment')
        # defaults = {'type':0, 'ordered':[], 'comment':''}
        # Angle = make_class(class_name, slots, defaults=defaults)
        return self.Angle()


class Dihedrals(dict):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.style: str = ''
        
        class_name = 'Dihedral'
        slots = ('type', 'ordered', 'comment')
        defaults = {'type':0, 'ordered':[], 'comment':''}
        self.Dihedral = make_class(class_name, slots, defaults=defaults)
        
    def dihedral_factory(self):
        # class_name = 'Dihedral'
        # slots = ('type', 'ordered', 'comment')
        # defaults = {'type':0, 'ordered':[], 'comment':''}
        # Dihedral = make_class(class_name, slots, defaults=defaults)
        return self.Dihedral()


class Impropers(dict):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.style: str = ''
        
        
        class_name = 'Improper'
        slots = ('type', 'ordered', 'comment')
        defaults = {'type':0, 'ordered':[], 'comment':''}
        self.Improper = make_class(class_name, slots, defaults=defaults)
        
    def improper_factory(self):
        # class_name = 'Improper'
        # slots = ('type', 'ordered', 'comment')
        # defaults = {'type':0, 'ordered':[], 'comment':''}
        # Improper = make_class(class_name, slots, defaults=defaults)
        return self.Improper()



