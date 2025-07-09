# -*- coding: utf-8 -*-
"""
@author: Tristan Muzzy
"""
import mooonpy

# file = mooonpy.Path('../EPON_862/system1_cell_replicate.data')
file = mooonpy.Path('../../../big_files/input/PBZ_cured_unwrapped.data')
# file = mooonpy.Path('../../../big_files/input/ringtest.data')
# file = mooonpy.Path('../../../big_files/input/sheet.data')

system = mooonpy.Molspace(file)
system.atoms.wrap()

# domains, pairs = system.compute_pairs(2,periodicity='ppp')
# cutoff = 2
# domains, fractionals = mooonpy.molspace.distance.domain_decomp_13(system.atoms, cutoff)
# pairs = mooonpy.molspace.distance.pairs_from_domains(system.atoms, cutoff, domains, fractionals)
# print(len(pairs))

bonds =system.compute_bond_length()


#
# for key, bond in bonds.items():
#     pair = pairs[key]
#     if abs(pair.distance - bond.distance) >0.000001: # float error
#         print(key, pair.distance, bond.distance)
#         raise Exception
