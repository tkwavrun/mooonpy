# -*- coding: utf-8 -*-
"""
@author: Josh Kemppainen
Revision 1.0
June 26, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931
"""
# Function for stringing together float values for parameters
def string_parameters(coeff):
    string = ''
    for i in coeff:
        if isinstance(i, float):
            string += '{:>16.10f}'.format(i)
        elif isinstance(i, int):
            string += '{:>6}'.format(i)
        else:
            string += '{:>6}'.format(i)
    return string
  

# Function for writing lammps datafile
def write(mol, filename):
        
    with open(filename,'w') as f: 
        # Write header
        header = mol.header
        f.write(f'# {header[-220:len(header)]}\n') # Make max header length of 220 characters 
            
        # Write all sections that have the "Coeffs ending"
        potentials = [i for i in dir(mol.ff) if i.endswith('coeffs')]
        write_order = ['pair_coeffs', 'bond_coeffs', 'angle_coeffs', 'dihedral_coeffs', 'improper_coeffs', 
                       'bondbond_coeffs', 'bondangle_coeffs', 'angleangletorsion_coeffs', 'endbondtorsion_coeffs',
                       'middlebondtorsion_coeffs', 'bondbond13_coeffs', 'angletorsion_coeffs', 'angleangle_coeffs']
        
        
        write_order = {'pair_coeffs':'pair_coeff',
                       'bond_coeffs': 'bond_coeff',
                       'angle_coeffs': 'angle_coeff',
                       'dihedral_coeffs': 'dihedral_coeff',
                       'improper_coeffs': 'improper_coeff',
                       
                       'bondbond_coeffs': 'angle_coeff {:^6}'.format('bb'),
                       'bondangle_coeffs': 'angle_coeff {:^6}'.format('ba'),
                       }
        
        
        styles = {'bond_coeffs': {'name':'bond_style', 'per-line':set([])},
                  'angle_coeffs': {'name':'angle_style', 'per-line':set([])},
                  'dihedral_coeffs': {'name':'dihedral_style', 'per-line':set([])},
                  'improper_coeffs': {'name':'improper_style', 'per-line':set([])},
                  
                  'pair_coeffs': {'name':'pair_style', 'per-line':set([])}
                  }
        
        
        # We need to check for hybrid styling to know how to write the
        # LAMMPS styles and the force field parameter secitons
        for attr in write_order:
            if attr not in potentials:
                print('WARNING potential: {} is not being written to {}.'.format(attr, filename))
                print(__file__)
                continue
            
            potential = getattr(mol.ff, attr)            
            type_ids = sorted(potential.keys())
            lmp_name = write_order[attr]
            for i in type_ids: 
                coeff = potential[i] 
                if attr in styles:
                    styles[attr]['per-line'].add(coeff.style)
                
        
        # Write LAMMPS force field style setup
        sections = 50*'-'
        f.write('\n\n{}{}{}\n'.format(sections, 'Force Field', sections))
        for i in styles:
            name = styles[i]['name']
            per_line = sorted(styles[i]['per-line'])
            if len(per_line) > 1:
                style = 'hybrid {}'.format(' '.join(per_line))
            else:
                style = '{}'.format(' '.join(per_line))
                
            if name == 'pair_style':
                f.write('{:<20} {} # PLEASE CHECK I AM CORRECT\n'.format('special_bonds', 'lj/coul 0 0 1'))
                
                style = '{}'.format(' '.join(['{} 12.0'.format(i) for i in per_line]))
                f.write('\n')
                f.write('{:<20} {}\n'.format(name, style))
                f.write('{:<20} {}\n'.format('kspace_style', 'pppm 1.0e-4'))
                if 'class2' in style:
                    f.write('{:<20} {}\n'.format('pair_modify', 'mix sixthpower'))
                elif 'charmm' in style:
                    f.write('{:<20} {}\n'.format('pair_modify', 'mix arithmetic'))   
                else:
                    f.write('{:<20} {} # PLEASE CHECK I AM CORRECT\n'.format('pair_modify', 'mix arithmetic'))   
                    f.write('\n')
            else:
                f.write('{:<20} {}\n'.format(name, style))
                
        # Finally write the force field parameters and some sort of neighbor list settings
        f.write('\n')
        f.write('{:<20} {}\n'.format('neighbor', '2.0 bin'))
        f.write('{:<20} {}\n'.format('neigh_modify', 'delay 0 every 1 check yes one 5000 page 100000'))
        
        
        # We will hold off writing each line till we can setup the force field styles
        for attr in write_order:
            potential = getattr(mol.ff, attr)            
            f.write('\n\n{}{}{}\n'.format(sections, potential.keyword, sections))

            type_ids = sorted(potential.keys())
            lmp_name = write_order[attr]
            for i in type_ids: 
                coeff = potential[i]
                parms = coeff.coeffs
                if coeff.comment:
                    comment = '# {}'.format(coeff.comment)
                else: comment = ''
                
                if attr in styles and len(styles[attr]['per-line']) > 1:
                    style = coeff.style
                else: style = ''
                
                f.write(('{} {:^10} {} {} {}\n'.format(lmp_name, i, style, string_parameters(parms), comment)))