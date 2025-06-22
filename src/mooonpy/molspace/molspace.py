# -*- coding: utf-8 -*-
"""
This will house the ability to generate molspace objects
"""
import sys



class Molspace:
    """
    MOLSPACE DOC STRING
    """
    def __init__(self):
        self.filename = 'TESTING.EXT'
        
        
# class Atoms1: pass

# class Atoms2:
#     def __init__(self):
#         self.x: float = 0.0
#         self.y: float = 0.0
#         self.z: float = 0.0
        
# atom1 = Atoms1()
# atom1.x: float = 0.0
# atom1.y: float = 0.0
# atom1.z: float = 0.0
# print('\n\nAtoms1')
# print(dir(atom1))
# print(sys.getsizeof(atom1))
# print(atom1.__dict__)
# print(atom1.__doc__)

# atom2 = Atoms2()
# print('\n\nAtoms2')
# print(dir(atom2))
# print(sys.getsizeof(atom2))
# print(atom2.__dict__)


# name = 'Atom3'
# bases = ()
# attrs = {'x': 0.0, 'y': 0.0, 'z': 0.0}
# atom3 = type(name, bases, attrs)
# print('\n\nAtoms3')
# print(dir(atom3))
# print(sys.getsizeof(atom3))
# print(atom3.__dict__)



# _class_cache = {}
# def get_class(name='Atoms'):
#     if name not in _class_cache:
#         cls = type(name, (), {'__slots__': ('x', 'y', 'z')})  # fixed behavior
#         _class_cache[name] = cls
#     return _class_cache[name]


# Atoms = get_class()
# atom4 = Atoms()
# atom4.x: float = 0.0
# atom4.y: float = 0.0
# atom4.x: float = 0.0
# print('\n\nAtoms4')
# print(dir(atom4))
# print(sys.getsizeof(atom4))
# print(atom4.__slots__)



# class Atoms5:
#     __slots__ = ('x', 'y', 'z')
#     __doc__ = None
#     def __init__(self):
#         self.x: float = 0.0
#         self.y: float = 0.0
#         self.z: float = 0.0

# atom5 = Atoms5()   
# print('\n\nAtoms5')
# print(dir(atom5))
# print(sys.getsizeof(atom5))
# #print(atom5.__slots__)
# #print(atom5.__doc__)
# for attr in dir(atom5):
#     value = getattr(atom5, attr)
#     print(attr, value, sys.getsizeof(value))
