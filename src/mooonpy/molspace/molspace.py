# -*- coding: utf-8 -*-
"""
@author: Josh Kemppainen
Revision 1.0
June 15, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931
"""
# from .box import Box
# from .atoms import Atoms
# from .bonds import Bonds
# from .force_field import ForceField
# from . import read_lmp_data as read_lmp_data



class Molspace():
    """
    Molspace doc string
    """
    def __init__(self, **kwargs):
        
        # Build this object with some composition
        # self.box: Box = Box()
        # self.atoms: Atoms = Atoms()
        # self.bonds: Bonds = Bonds()
        # self.force_field: ForceField = ForceField()
        
        # # Test some composition
        # print('Box xlo, xhi: ', self.box.xlo, self.box.xhi)
        # print('atoms = ', self.atoms)
        # print('bonds = ', self.bonds)
        # print('masses = ', self.force_field.masses)
        
        # Setup file reading based on keyword arguments
        self.filename: str = ''
        if 'file' in kwargs:
            filename = kwargs['file']
            self.read_files(filename)
            
            print('Updated filename = ', self.filename)
            print('Updated atoms = ', self.atoms)


                
    def read_files(self, filename):
        """

        Parameters
        ----------
        filename : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # self.filename: str = filename
        # if filename.endswith('.data'):
        #     read_lmp_data.read(self, filename)
            
    def write_files(self, filename):
        """

        Parameters
        ----------
        filename : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        pass
        
        
    def printme(self, string):
        print(string)
        

