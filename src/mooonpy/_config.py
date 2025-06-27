# -*- coding: utf-8 -*-


# mooonpy/_config.py
from collections.abc import MutableMapping

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
_defaults = {'color': 'blue',
             'linewidth': 2,     
             'fontsize': 12,
             'molspace.read.dsect': ['Atoms', 'Bonds', 'Angles', 'Dihedrals', 'Impropers', 'Velocities'],
             'molspace.astyles': ['all']
}

rcParams = RCParams(_defaults)