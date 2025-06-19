
def generate_a_molspace() -> None:
    """
    Example how to generate a molecular system using molspace
    
    from mooonpy import molspace as ms
    
    detda = ms.molspace(file='../DETDA.mol2')
    

    :return: None
    :rtype: None
    """
    return None


def modify_a_molspace() -> None:
    """
    Example how to modify a molecular system using molspace
    
    from mooonpy import molspace as ms
    
    detda = ms.molspace(file='../DETDA.mol2')
    detda.atoms.shift(x=5, y=10, z=15)
    detda.atoms.rot(rx=45, ry=90, rz=0)
    
    detda.parameterize(ff='PCFF', frc='../frc_files/pcff.py')
    

    :return: None
    :rtype: None
    """
    return None