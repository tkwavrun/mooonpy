# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 16:03:17 2025

@author: jdkem
"""

import mooonpy
from mooonpy import molspace as ms
from mooonpy import thermospace as ts



print('full : ', mooonpy.molspace.hello_world())
print('alias: ', ms.hw.hello_world())


print('full : ', mooonpy.thermospace.multiply(x=5, y=10))
print('alias: ',  ts.lw.multiply(x=5, y=10))
