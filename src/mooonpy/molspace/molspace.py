# -*- coding: utf-8 -*-
from . import _files_io as _files_io
from .atoms import Atoms
from .topology import Bonds, Angles, Dihedrals, Impropers
from .force_field import ForceField
from ..rcsetup import rcParams
import os


class Molspace(object):
    """
    Initializes a Molspace instance
    -------------------------------
    
    This class can be called via:
      * Full namespace syntax    : ``mooonpy.molspace.molspace.Molspace()``
      * Aliased namespace syntax : ``mooonpy.Molspace()``
    """
    def __init__(self, filename='', **kwargs):
        """        
        Initialization Parameters
        -------------------------
        filename : str, optional
            An optional filename to read and initialize a Molspace() instance
            with molecular system information (e.g. atoms, bonds, force field
            parameters ...). Supported file extensions:
                
              * LAMMPS datafile ``.data``
              * Tripos mol2 file ``.mol2``
              * SYBL mol file ``.mol``
        
            If no filename is provided the Molspace instance will be generated
            with no molecular system information.
            
            
        Attributes
        ----------
        N : int
            The order of the filter. For 'bandpass' and 'bandstop' filters,
            the resulting order of the final second-order sections ('sos')
            matrix is ``2*N``, with `N` the number of biquad sections
            of the desired system.
        Wn : array_like
            The critical frequency or frequencies. For lowpass and highpass
            filters, Wn is a scalar; for bandpass and bandstop filters,
            Wn is a length-2 sequence.
            
        Methods
        -------
        N : int
            The order of the filter. For 'bandpass' and 'bandstop' filters,
            the resulting order of the final second-order sections ('sos')
            matrix is ``2*N``, with `N` the number of biquad sections
            of the desired system.
        """
        
        print(rcParams)
        
        # Get some basic config options from kwargs or setup defaults
        #print(kwargs)
        
        self.astyles = kwargs.pop('astyles', rcParams['molspace.astyles'])
        self.dsect = kwargs.pop('dsect', rcParams['molspace.read.dsect'])
        
        #print(kwargs)
        
        # Build this object with some composition
        self.atoms: Atoms = Atoms(self.astyles)
        self.bonds: Bonds = Bonds()
        self.angles: Angles = Angles()
        self.dihedrals: Dihedrals = Dihedrals()
        self.impropers: Impropers = Impropers()
        self.ff: ForceField = ForceField()

        # Handle file initilaizations
        self.filename = filename
        self.header = ''
        if filename:
            if not self.filename:
                pass
            
            if not os.path.exists(filename):
                raise FileNotFoundError(f'{filename} was not found or is a directory')
            
            self.read_files(filename, dsect=self.dsect) 
            
    
        #keys = self.bonds

                
        

        
    def read_files(self, filename, dsect=['all']):
        root, ext = os.path.splitext(filename)     
        if filename.endswith('.data'):
            if 'all' in dsect:
                dsect = ['Atoms', 'Bonds', 'Angles', 'Dihedrals', 'Impropers', 'Velocities']
            _files_io.read_lmp_data.read(self, filename, dsect)
            
        return None
    
    def write_files(self, filename, atom_style='full'):
        root, ext = os.path.splitext(filename)     
        if filename.endswith('.data'):
            _files_io.write_lmp_data.write(self, filename, atom_style)
        
        
