# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 11:33:04 2025

@author: jdkem
"""
from ...tools import file_utils
import time
import timeit



def read(mol, filename, config):
    
    # Define sections to read (using inputs from user if they pass them)
    sections_mp:    list[str] = ['Atoms', 'Bonds', 'Angles', 'Dihedrals', 'Impropers', 'Velocities', 'Ellipsoids', 'Lines', 'Triangles', 'Bodies']
    sections_tl:    list[str] = ['Atom Type Labels', 'Bond Type Labels', 'Angle Type Labels', 'Dihedral Type Labels', 'Improper Type Labels']
    sections_ff:    list[str] = ['Masses', 'Pair Coeffs', 'Bond Coeffs', 'Angle Coeffs', 'Dihedral Coeffs', 'Improper Coeffs', 'PairIJ Coeffs']
    sections_xt:    list[str] = ['BondBond Coeffs', 'BondAngle Coeffs', 'AngleAngleTorsion Coeffs', 'EndBondTorsion Coeffs', 
                                 'MiddleBondTorsion Coeffs', 'BondBond13 Coeffs', 'AngleTorsion Coeffs', 'AngleAngle Coeffs']
    sections_fixes: list[str] = ['bond_react_props_internal']
    
    # Setup the sets that will be used for parsing
    sections_all:    set[str] = set(sections_mp + sections_tl + sections_ff + sections_xt + sections_fixes)
    sections_coeffs: set[str] = sections_ff + sections_xt
    sections_kwargs: set[str] = set(config['sections'])
    
    
    # Find "hard coded" atom style reads for performance
    hard_coded_atom_styles = {i.split('_')[-1]:i for i in dir(mol.atoms.styles) if i.startswith('atoms_')}
    
    
    # Create shortcuts to all the generation factories for speed and ease of use
    atom_factory = mol.atoms.styles.gen_atom
    bond_factory = mol.bonds.gen_bond()
    angle_factory = mol.angles.gen_angle()
    dihedral_factory = mol.dihedrals.gen_dihedral()
    improper_factory = mol.impropers.gen_improper()
    
    
    # Open and read contents from file
    skip: int = 0
    section: str = ''
    ff_coeffs: None = None # Will be a pointer to specifc ff_coeffs to update
    with file_utils.smart_open(filename) as f:
        #f = f.readlines()
        for n, string in enumerate(f):
            skip -= 1
            string = string.strip()
            
            # skip line between section keywords and "top of the body"
            if skip >= 0:
                continue
            
            # Toggle section "off" since a blank line will be at 
            # the "bottom of the body" (skip handles the blank line
            # at the "top of the body").
            elif not string:
                section = ''
                continue
            
            # Deal with comments
            elif '#' in string:
                line = string.split('#')
                data_str = line[0].strip()
                data_lst = data_str.split()
                comment = line[1].strip()
            else:
                data_str = string.strip()
                data_lst = data_str.split()
                comment = ''

            
            #-------------------------------------------------------#
            # Parse the computationally heavy parts 1st:            #
            #  - setting the section requires looking at each line  #
            #  - if we already know the section we can get extra    #
            #    performance by not having to set section flag for  #
            #    the entire strech of the large sections            #
            #-------------------------------------------------------#
            if section == 'Atoms':
                atom = atom_factory() #mol.atoms.styles.gen_atom()
                mol.atoms.styles.fill_atom(atom, mol.atoms.style, data_lst)
                mol.atoms[atom.id] = atom
                
            elif section == 'Bonds':
                #ID = int(data_lst[0])
                typeID = file_utils.string2digit(data_lst[1]) # This  could be a type label
                id1 = int(data_lst[2])
                id2 = int(data_lst[3])
                
                bond = bond_factory #mol.bonds.gen_bond()
                bond.ordered = [id1, id2]
                bond.comment = comment
                bond.type = typeID
                mol.bonds[(id1, id2)] = bond
                
            elif section == 'Angles':
                #ID = int(data_lst[0])
                typeID = file_utils.string2digit(data_lst[1]) # This  could be a type label
                id1 = int(data_lst[2])
                id2 = int(data_lst[3])
                id3 = int(data_lst[4])
                
                angle = angle_factory #mol.angles.gen_angle()
                angle.ordered = [id1, id2, id3]
                angle.comment = comment
                angle.type = typeID
                mol.angles[(id1, id2, id3)] = angle
                
            elif section == 'Dihedrals':
                #ID = int(data_lst[0])
                typeID = file_utils.string2digit(data_lst[1]) # This  could be a type label
                id1 = int(data_lst[2])
                id2 = int(data_lst[3])
                id3 = int(data_lst[4])
                id4 = int(data_lst[5])
                
                dihedral = dihedral_factory #mol.dihedrals.gen_dihedral()
                dihedral.ordered = [id1, id2, id3, id4]
                dihedral.comment = comment
                dihedral.type = typeID
                mol.dihedrals[(id1, id2, id3, id4)] = dihedral
                
            elif section == 'Impropers':
                #ID = int(data_lst[0])
                typeID = file_utils.string2digit(data_lst[1]) # This  could be a type label
                id1 = int(data_lst[2])
                id2 = int(data_lst[3])
                id3 = int(data_lst[4])
                id4 = int(data_lst[5])
                
                improper = improper_factory #mol.impropers.gen_improper()
                improper.ordered = [id1, id2, id3, id4]
                improper.comment = comment
                improper.type = typeID
                mol.impropers[(id1, id2, id3, id4)] = improper
            
            
            # Type labels can initialize a ff_coeffs build
            elif section in sections_tl and ff_coeffs is not None:
                typeID = int(data_lst[0])
                type_label = str(data_lst[1])
                
                params = ff_coeffs.gen_params()
                params.comment = type_label
                params.type_label = type_label
                ff_coeffs[typeID] = params
            
            
            # Read-in force field parameters (type labels might have already initialized a 
            # ff_coeffs build - if not one will be initialized here)
            elif section in sections_coeffs and ff_coeffs is not None:
                #print(n, line, section)
                digits = [file_utils.string2digit(string) for string in data_lst]
                typeID = digits[0]
                coeffs = digits[1:]
                if typeID in ff_coeffs:
                    ff_coeffs[typeID].coeffs = coeffs
                else:
                    # Build type label from comment, if type label
                    # doesnt already exist or set as read-in typeID
                    if comment:
                        type_label = comment
                    else:
                        type_label = str(typeID)
                        
                    # Generate a params instance and add to it 
                    params = ff_coeffs.gen_params(coeffs)
                    params.comment = comment
                    params.type_label = type_label
                    ff_coeffs[typeID] = params  
                   
            # Get box dimensions
            elif 'xlo' in data_str and 'xhi' in data_str:
                mol.atoms.box.xlo = float(data_lst[0]) 
                mol.atoms.box.xhi = float(data_lst[1]) 
            elif 'ylo' in data_str and 'yhi' in data_str:
                mol.atoms.box.ylo = float(data_lst[0]) 
                mol.atoms.box.yhi = float(data_lst[1]) 
            elif 'zlo' in data_str and 'zhi' in data_str:
                mol.atoms.box.zlo = float(data_lst[0]) 
                mol.atoms.box.zhi = float(data_lst[1]) 
            elif 'xy' in data_str and 'xz' in data_str and 'yz' in data_str:
                mol.atoms.box.xy = float(data_lst[0]) 
                mol.atoms.box.xz = float(data_lst[1]) 
                mol.atoms.box.yz = float(data_lst[2])               
            elif n == 0: mol.header = string

                
            #-----------------------------------------------------------------#
            # Toggle between sections. Toggling is expensive:                 #
            #  - Requires each line to be check, which means every line in    #
            #    Atoms, Bond, ... etc needs to be checked                     #
            #  - If we use wise if/elif settings, once the Atoms, Bonds, ...  #
            #    etc sections have been found we do not have to check         #
            #    if data_str is a section to parse                            #
            #-----------------------------------------------------------------#
            #elif data_str in sections_all:
            elif data_str[0].isalpha():
                skip = 1 # skip the line under each section keyword
                section = data_str
                if section not in sections_all:
                    raise Exception(f'ERROR {section} is not a supported LAMMPS datafile section')
                
                # Set flags for molecule data like atoms, bonds, etc ... Also check if user wants
                # that section read or not (if not set section to '', to skip reading that section)
                if section == 'Atoms':
                    mol.atoms.style = comment
                    if 'Atoms' not in sections_kwargs:
                        section = ''
                elif section == 'Bonds' and 'Bonds' not in sections_kwargs:
                    section = ''
                elif section == 'Angles' and 'Angles' not in sections_kwargs:
                    section = ''
                elif section == 'Dihedrals' and 'Dihedrals' not in sections_kwargs:
                    section = ''
                elif section == 'Impropers' and 'Impropers' not in sections_kwargs:
                    section = ''
                elif section == 'Velocities' and 'Velocities' not in sections_kwargs:
                    section = ''
    
                # Type labels can initialize a ff dictionary (e.g. Atom Type
                # Labels, will generate the mol.ff.masses and then once masses
                # are ready, the coeffs will be updated at that point).
                elif section == 'Atom Type Labels':
                    ff_coeffs = mol.ff.masses
                elif section == 'Bond Type Labels':
                    ff_coeffs = mol.ff.bond_coeffs
                elif section == 'Angle Type Labels':
                    ff_coeffs = mol.ff.angle_coeffs
                elif section == 'Dihedral Type Labels':
                    ff_coeffs = mol.ff.dihedral_coeffs
                elif section == 'Improper Type Labels':
                    ff_coeffs = mol.ff.improper_coeffs
                
                # Force field related parsing
                elif section == 'Masses':
                    ff_coeffs = mol.ff.masses
                    ff_coeffs.style = comment
                elif section == 'Pair Coeffs':
                    ff_coeffs = mol.ff.pair_coeffs
                    ff_coeffs.style = comment
                elif section == 'Bond Coeffs':
                    ff_coeffs = mol.ff.bond_coeffs
                    ff_coeffs.style = comment
                elif section == 'Angle Coeffs':
                    ff_coeffs = mol.ff.angle_coeffs
                    ff_coeffs.style = comment
                elif section == 'Dihedral Coeffs':
                    ff_coeffs = mol.ff.dihedral_coeffs
                    ff_coeffs.style = comment
                elif section == 'Improper Coeffs':
                    ff_coeffs = mol.ff.improper_coeffs
                    ff_coeffs.style = comment
                elif section == 'BondBond Coeffs':
                    ff_coeffs = mol.ff.bondbond_coeffs
                    ff_coeffs.style = comment
                elif section == 'BondAngle Coeffs':
                    ff_coeffs = mol.ff.bondangle_coeffs
                    ff_coeffs.style = comment
                elif section == 'AngleAngleTorsion Coeffs':
                    ff_coeffs = mol.ff.angleangletorsion_coeffs
                    ff_coeffs.style = comment
                elif section == 'EndBondTorsion Coeffs':
                    ff_coeffs = mol.ff.endbondtorsion_coeffs
                    ff_coeffs.style = comment
                elif section == 'MiddleBondTorsion Coeffs':
                    ff_coeffs = mol.ff.middlebondtorsion_coeffs
                    ff_coeffs.style = comment
                elif section == 'BondBond13 Coeffs':
                    ff_coeffs = mol.ff.bondbond13_coeffs
                    ff_coeffs.style = comment
                elif section == 'AngleTorsion Coeffs':
                    ff_coeffs = mol.ff.angletorsion_coeffs
                    ff_coeffs.style = comment
                elif section == 'AngleAngle Coeffs':
                    ff_coeffs = mol.ff.angleangle_coeffs
                    ff_coeffs.style = comment
                else:
                    # We need to toggle ff_coeffs between different sections
                    # so we do not add coeffs to the wrong dictionaries
                    ff_coeffs = None
                continue
            



                

                
            

            

    
    # print('\n\n\nSTYLES:')
    # print('header: ', mol.header[:50])
    # print('atom style: ', mol.atoms.style)
    # print('xbox: ', mol.atoms.box.xlo, mol.atoms.box.xhi)
    # print('ybox: ', mol.atoms.box.ylo, mol.atoms.box.yhi)
    # print('zbox: ', mol.atoms.box.zlo, mol.atoms.box.zhi)
    # print('tilt: ', mol.atoms.box.xy, mol.atoms.box.xz, mol.atoms.box.yz)
    # print('natoms: ', len(mol.atoms))
    # print('nbonds: ', len(mol.bonds))
    # print('nangles: ', len(mol.angles))
    # print('ndihedrals: ', len(mol.dihedrals))
    # print('nimpropers: ', len(mol.impropers))
    
    # print('\n\nAtoms')
    # for n, (key, value) in enumerate(mol.atoms.items()):
    #     if n < 5:
    #         print(key, value.type, value.x, value.y, value.z, value.comment)
    # # line = mol.atoms.styles.gen_line(mol.atoms[1], style='body')
    # # print(line)
    
    # print('\n\nBonds')
    # for n, (key, value) in enumerate(mol.bonds.items()):
    #     if n < 5:
    #         print(key, value.type, value.ordered, value.bo, value.comment)
            
    # print('\n\nAngles')
    # for n, (key, value) in enumerate(mol.angles.items()):
    #     if n < 5:
    #         print(key, value.type, value.ordered, value.bo, value.comment)
            
    # print('\n\nDihedrals')
    # for n, (key, value) in enumerate(mol.dihedrals.items()):
    #     if n < 5:
    #         print(key, value.type, value.ordered, value.bo, value.comment)
            
    # print('\n\nImpropers')
    # for n, (key, value) in enumerate(mol.impropers.items()):
    #     if n < 5:
    #         print(key, value.type, value.ordered, value.bo, value.comment)
    
    # d = mol.ff.masses
    # # d = mol.ff.pair_coeffs
    # # d = mol.ff.bond_coeffs
    # # d = mol.ff.angle_coeffs
    # # d = mol.ff.dihedral_coeffs
    # # d = mol.ff.improper_coeffs
    # # d = mol.ff.bondbond_coeffs
    # # d = mol.ff.bondangle_coeffs
    # # d = mol.ff.angleangletorsion_coeffs
    # # d = mol.ff.endbondtorsion_coeffs
    # # d = mol.ff.middlebondtorsion_coeffs
    # # d = mol.ff.bondbond13_coeffs
    # # d = mol.ff.angletorsion_coeffs
    # # d = mol.ff.angleangle_coeffs
    # print('\n\nFF-CHECK: ', d.style)
    # for key, value in d.items():
    #     print('{} {}   "{}"   "{}"'.format(key, value.coeffs, value.type_label, value.comment))
        

            

        

            
        