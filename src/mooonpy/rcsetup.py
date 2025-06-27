# -*- coding: utf-8 -*-


# mooonpy/_config.py
from collections.abc import MutableMapping


# Matplotlib GitHub:
#    https://github.com/matplotlib/matplotlib/blob/main/lib/matplotlib/rcsetup.py
#    https://github.com/matplotlib/matplotlib/blob/main/lib/matplotlib/__init__.py
class RCParams(MutableMapping):
    def __init__(self, defaults):
        self._params = dict(defaults)

    def __getitem__(self, key):
        return self._params[key]

    def __setitem__(self, key, value):
        self._params[key] = value

    def __delitem__(self, key):
        del self._params[key]

    def __iter__(self):
        return iter(self._params)

    def __len__(self):
        return len(self._params)

    def update(self, new_params):
        self._params.update(new_params)

    def reset(self):
        self._params = dict(self._defaults)

    def __str__(self):
        return str(self._params)

# Default parameters
_defaults = {'molspace.read.dsect': ['Atoms', 'Bonds', 'Angles', 'Dihedrals', 'Impropers', 'Velocities'],
             'molspace.write.data.astyle': 'full',
             'molspace.astyles': ['all'],
             
             'thermospace.read': 'all',
             
             'xrdspace.read': 'all'
}

rcParams = RCParams(_defaults)


if __name__ == "__main__": 
    print(rcParams.get('help'))
    print(rcParams.get('molspace.write.data.astyle'))