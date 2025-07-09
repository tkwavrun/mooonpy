# -*- coding: utf-8 -*-
"""
miscellaneous utilities that do not belong anywhere else
"""
from .tables import ListListTable
from .file_utils import Path


class ColorMap(ListListTable):
    """
    Read csv files of RGB values with a similar format to matplotlib.colormaps.
    root/tools/lookups contains some exaple custom colormaps, more can be added by adding files to this directory.

    **Currently Supported Colormaps**
        - coolwarm: blue to light to red diverging map (same as matplotlib?)
        - cooloverwarm: blue to grey to red diverging map
        - coswan: pink to grey to green diverging map
        - pyrolyze: green to grey to dark purple diverging map
        - redblack: red to dark grey linearish map
    """
    def __init__(self, name='coolwarm'):
        """
        Read csv files of RGB vales into a ListListTable object.
        """
        super().__init__()
        thisfile = Path(__file__)
        parent = ListListTable.read_csv(thisfile.dir()/f'lookups/{name}.csv',True,True)
        self.__dict__.update(parent.__dict__)
        self.name = name

    def __call__(self,scalar):
        """
        Return nearest color on 0-1 scale
        """
        if isinstance(scalar, float):
            if scalar <= 0:
                row_ind = 0
            elif scalar >= 1:
                row_ind = -1
            else:
                row_ind = int(scalar*(len(self.grid)-1))
            return tuple(self.grid[row_ind])
        elif isinstance(scalar, int):
            return tuple(self.grid[scalar])
        else: # iterable
            for scalar_ in scalar:
                out = []
                if scalar_ <= 0:
                    row_ind = 0
                elif scalar_ >= 1:
                    row_ind = -1
                else:
                    row_ind = int(scalar_ * (len(self.grid) - 1))
                out.append(tuple(self.grid[row_ind]))
            return out