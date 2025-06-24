# -*- coding: utf-8 -*-



class Nbody():  
    __slots__ = ('bo', 'type', 'ordered', 'comment')
    def __init__(self):
        self.bo: float = 0.0
        self.type: int = 0
        self.ordered: list[int] = []
        self.comment: str = ''
        
        
class Bonds(dict):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def gen_bond(self):
        bond: Nbody = Nbody()
        return bond
    
    
class Angles(dict):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def gen_angle(self):
        angle: Nbody = Nbody()
        return angle



class Dihedrals(dict):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def gen_dihedral(self):
        dihedral: Nbody = Nbody()
        return dihedral



class Impropers(dict):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def gen_improper(self):
        improper: Nbody = Nbody()
        return improper



