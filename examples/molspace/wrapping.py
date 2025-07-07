# -*- coding: utf-8 -*-
"""
@author: Tristan Muzzy
"""
import mooonpy
import subprocess

file = '../../../big_files/input/PBZ_cured_unwrapped.data'
molecule = mooonpy.Molspace(file)
molecule.atoms.wrap()
outfile = '../../../big_files/output/PBZ_cured_wrapped.data'
molecule.write_files(outfile,atom_style='full')
# subprocess.call((mooonpy.rcParams['OVITO'],outfile)) # this should be aliased somewhere.
