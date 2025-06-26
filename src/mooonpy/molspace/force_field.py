# -*- coding: utf-8 -*-


class Parameters(object):
    def __init__(self, coeffs):                
        self.coeffs: list = coeffs
        self.comment: str = ''
        self.type_label: str = ''


class Coefficients(dict):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        self.style: str = ''
        

class ForceField(object):
    def __init__(self, **kwargs):
        # Build this object with some composition
        self.masses: Coefficients = Coefficients() # {type : Parameters-object}
        self.pair_coeffs: Coefficients = Coefficients() # {type : Parameters-object}
        
        self.bond_coeffs: Coefficients = Coefficients() # {type : Parameters-object}
        self.angle_coeffs: Coefficients = Coefficients() # {type : Parameters-object}
        self.dihedral_coeffs: Coefficients = Coefficients() # {type : Parameters-object}
        self.improper_coeffs: Coefficients = Coefficients() # {type : Parameters-object}

        self.bondbond_coeffs: Coefficients = Coefficients() # {type : Parameters-object}
        self.bondangle_coeffs: Coefficients = Coefficients() # {type : Parameters-object}
        self.angleangletorsion_coeffs: Coefficients = Coefficients() # {type : Parameters-object}
        self.endbondtorsion_coeffs: Coefficients = Coefficients() # {type : Parameters-object}
        self.middlebondtorsion_coeffs: Coefficients = Coefficients() # {type : Parameters-object}
        self.bondbond13_coeffs: Coefficients = Coefficients() # {type : Parameters-object}        
        self.angletorsion_coeffs: Coefficients = Coefficients() # {type : Parameters-object}
        self.angleangle_coeffs: Coefficients = Coefficients() # {type : Parameters-object}
        
        
    def coeffs_factory(self, coeffs=None):
        if coeffs is None: coeffs = []
        return Parameters(coeffs)

        
