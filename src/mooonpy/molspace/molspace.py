# -*- coding: utf-8 -*-
from . import _files_io as _files_io
from .atoms import Atoms
from .topology import Bonds, Angles, Dihedrals, Impropers
from .force_field import ForceField
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
        
        # kwargs = {'astyles':['full', 'charge'], 'b':2, 'c':3}
        
        # print('kwargs = ', kwargs)
        
        # defaults = {'astyles':['all'],
        #             'b': None,
        #             'lmp_sections': ['Atoms', 'Bonds', 'Angles', 'Dihedrals', 'Impropers', 'Velocities']
        #             }
        # print('defaults =', defaults)
        
        # config = {**defaults, **kwargs} 
        # print('config = ', config)
        
        # Build this object with some composition
        self.atoms: Atoms = Atoms()
        self.bonds: Bonds = Bonds()
        self.angles: Angles = Angles()
        self.dihedrals: Dihedrals = Dihedrals()
        self.impropers: Impropers = Impropers()
        self.ff: ForceField = ForceField()

        # Handle file initilaizations
        self.filename = filename
        self.header = ''
        if filename:
            if os.path.exists(filename):
                self.read_files(filename, **kwargs)
            else:
                raise FileNotFoundError(f'{filename} was not found or is a directory')
        

        
    def read_files(self, filename, **kwargs):

        
        root, ext = os.path.splitext(filename)
        defaults = {'read':'mooonpy', 'sections':('Atoms', 'Bonds', 'Angles', 'Dihedrals', 'Impropers', 'Velocities')}
        config = {**defaults, **kwargs}        
        if filename.endswith('.data'):
            if 'data_sections' in kwargs:
                sections = kwargs['data_sections']
            else:
                sections = ('Atoms', 'Bonds', 'Angles', 'Dihedrals', 'Impropers', 'Velocities')
            
            if config['read'] == 'mooonpy':
                _files_io.read_lmp_data.read(self, filename, sections)
            else:
                _files_io.read_lmp.Molecule_File(filename, method='forward', sections=sections)
            
        return None
        
        
