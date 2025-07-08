# -*- coding: utf-8 -*-
"""
@author: Tristan Muzzy
"""
import mooonpy
import subprocess

file = mooonpy.Path('../EPON_862/system1_cell_replicate.data')
# file = mooonpy.Path('../../../big_files/input/PBZ_cured_unwrapped.data')

system = mooonpy.Molspace(file)
system.atoms.wrap()

# domains, pairs = system.compute_pairs(4)
cutoff = 2
domains, fractionals = mooonpy.molspace.distance.domain_decomp_13(system.atoms, cutoff)
pairs = mooonpy.molspace.distance.pairs_from_domains(system.atoms, cutoff, domains, fractionals)
print(len(pairs))
