# -*- coding: utf-8 -*-
import gzip
import bz2
import lzma
import glob
import os
import re


def is_float(string):
    float_re = re.compile(r'^-?\d+(\.\d+)?([eE][-+]?\d+)?$')
    return bool(float_re.match(string))

def string2digit(string):
    if string.isnumeric():
        return int(string)
    elif is_float(string):
        return float(string)
    else:
        return string

def smart_open(filename, mode='r', encoding='utf-8'):
    """
    Open file with appropriate compression based on extension
    """

    try:
        if '.gz' in filename:
            return gzip.open(filename, mode + 't', encoding=encoding)
        elif '.bz2' in filename:
            return bz2.open(filename, mode + 't', encoding=encoding)
        elif '.xz' in filename or '.lzma' in filename:
            return lzma.open(filename, mode + 't', encoding=encoding)
    except: pass # compressed filename did not work
    return open(filename, mode, encoding=encoding) # try regular read

# # Works with multiple compression types
# with smart_open(file) as f:
#     for line in f:
#         process(line)



class Path(str): ## I think topofile is OK for instances of path objects, but a more general word should be used to avoid mangleing and add precision
    ## __init__ is immutable for string
    def __new__(cls, string): ## this is before init somehow
        return super().__new__(cls,os.path.normpath(string))
    def __truediv__(self, other): # overrides string concatenate
        ## this did use + or __add__ but was changed to keep string addtion, slash already meas directory so it's better
        return Path(os.path.join(self, other))
    def __bool__(self):
        return os.path.exists(self)
    def __abs__(self):
        return Path(os.path.normpath(self)) ## change to abspath?
    def matches(self):
        out = [Path(file) for file in glob.glob(self)]
        return out
    def __iter__(self): ## iterating characters is useless, this gets matches
        # out =[Path(file) for file in glob.glob(self)]
        return iter(self.matches())
    def recent(self,oldest=False):
        ## finds most recently modified match in matches
        times = {}
        for file in self:
            times[os.path.getmtime(file)] = file
        if times:
            sorted_time = sorted(list(times.keys()))
            if oldest:
                return times[sorted_time[0]]
            else:
                return times[sorted_time[-1]]
        else:
            return None

    ## Make math operators for these functions. Or make attributes after each init?
    def dir(self):
        """

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return Path(os.path.dirname(self))
    def basename(self):
        """

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return Path(os.path.basename(self))
    def root(self):
        return Path(os.path.splitext(self.basename())[0])
    def ext(self):
        return Path(os.path.splitext(self.basename())[1])
    def new_ext(self,ext): ## same idea as topofile.bonds
        # self.new_ext('.mol') # '.' must be included
        # example.data -> example.mol
        return Path(os.path.splitext(self)[0]+ext)
    def open(self, mode='r', encoding='utf-8'):
        return smart_open(self, mode, encoding)
    
    
if __name__ == '__main__':
    print('Testing __main__')
    IO = Path('C:/Users/trist/OneDrive/Desktop/MMC')
    file = Path('molspace_a0_*.py')
    topofile = IO/file
    topofile = abs(topofile)
    print(topofile,bool(topofile))

    for ff in topofile:
        print(ff)
    print()
    L = list(file)
    print(L)
    print()
    example = Path('JDK_5May2025/Examples/detda_typed_PCFF.data')
    print(example)
    print(example.dir())
    print(example.basename())
    print(example.root())
    print(example.ext())
    print(example.new_ext('.mol'))