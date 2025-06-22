# -*- coding: utf-8 -*-
"""
@author: Josh Kemppainen
Revision 1.0
June 15, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931
"""


class Box:
    def __init__(self):
        self.xlo: float = -0.5
        self.xhi: float =  0.5
        self.ylo: float = -0.5
        self.yhi: float =  0.5
        self.zlo: float = -0.5
        self.zhi: float =  0.5
        self.yz: float = 0.0
        self.xz: float = 0.0
        self.xy: float = 0.0
        
    def get_lengths(self) -> list[float]:
        """
        Compute box lengths from box edges.
        """
        lx = self.xhi - self.xlo
        ly = self.yhi - self.ylo
        lz = self.zhi - self.zlo
        return [lx, ly, lz]
    
    def get_transformation_matrix(self) -> list[list[float]]:
        """
        Generate transformation matrix to convert to and from fractional 
        or Cartesian coordinates using LAMMPS "sparse matrix" setup.
        """
        lx, ly, lz = self.get_lengths()
        h = [lx, ly, lz, self.yz, self.xz, self.xy] 
        h_inv = 6*[0]
        h_inv[0] = 1/h[0]
        h_inv[1] = 1/h[1]
        h_inv[2] = 1/h[2]
        h_inv[3] = -h[3] / (h[1]*h[2])
        h_inv[4] = (h[3]*h[5] - h[1]*h[4]) / (h[0]*h[1]*h[2])
        h_inv[5] = -h[5] / (h[0]*h[1])
        
        # General box parameters
        boxlo = [self.xlo, self.ylo, self.zlo]
        boxhi = [self.xhi, self.yhi, self.zhi]
        return [h, h_inv, boxlo, boxhi]