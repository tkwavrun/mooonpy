# -*- coding: utf-8 -*-
from collections import defaultdict

from .atoms import Atoms
import math


class Domain(list):
    """
    Class to contain atoms within a domain as a list of atom IDs
    """

    def __init__(self, atom_list=None):
        if atom_list is None:
            atom_list = []
        super(Domain, self).__init__(atom_list)
        self.x: float = 0.0
        self.y: float = 0.0
        self.z: float = 0.0
        self.neighbors: dict = {}


class Pair():
    def __init__(self, dx, dy, dz, distance):
        self.dx: float = dx
        self.dy: float = dy
        self.dz: float = dz
        self.distance: float = distance


def pairs_from_domains(atoms, cutoff, domains, fractionals):
    if not isinstance(atoms, Atoms):
        raise TypeError('atoms must be a Atoms object')
    box = atoms.box
    h, h_inv, boxlo, boxhi = box.get_transformation_matrix()

    pairs = {}
    cutoff_pow2 = cutoff * cutoff

    for box_index, domain in domains.items():  # this can be parallelized
        for neighbor_index, image_shift in domain.neighbors.items():
            for atom_A in domain:  # in list
                ## setup 1 A atom at a time
                if image_shift == (0, 0, 0):  # no shift, get positions skipping box steps
                    Atom_A = atoms[atom_A]  # get class instance
                    pos_x = Atom_A.x
                    pos_y = Atom_A.y
                    pos_z = Atom_A.z
                else:  # get positions after shift
                    ux, uy, uz = fractionals[atom_A]
                    ux += image_shift[0]
                    uy += image_shift[1]
                    uz += image_shift[2]
                    pos_x, pos_y, pos_z = box.frac2pos(ux, uy, uz, h, boxlo)
                for atom_B in domains[neighbor_index]:
                    Atom_B = atoms[atom_B]  # get class instance
                    if atom_A == atom_B:
                        continue
                    elif atom_A < atom_B:  # from low to high
                        dx = Atom_B.x - pos_x
                        dy = Atom_B.y - pos_y
                        dz = Atom_B.z - pos_z
                    elif atom_A > atom_B:  # reverse vector
                        dx = pos_x - Atom_B.x
                        dy = pos_y - Atom_B.y
                        dz = pos_z - Atom_B.z
                    distance2 = dx * dx + dy * dy + dz * dz
                    if distance2 < cutoff_pow2:
                        key = sorted([atom_A, atom_B])
                        pairs[tuple(key)] = Pair(dx, dy, dz, math.sqrt(distance2))
    return pairs


def domain_decomp_13(atoms, cutoff, whitelist=None, blacklist=None, periodicity='ppp'):
    """
    Setup domains for pairwise distance computation. This uses a 3x3x3 grid, where each domain checks self
    and half of the 26 adjacent domains, hence 13 others. Checking order priority is -z, -x, -y (make image eventually)
    This algorithm is optimized for short cutoffs under ~5 angstroms. Longer cutoffs would be faster with a
    DD_62 algorithm similar to https://docs.lammps.org/Developer_par_neigh.html


    ..warning :: Atoms must be correctly wrapped before calling this function.
        Highly skewed triclinic does not currently set the minimum domain sizes correctly

    ..TODO :: Validate triclinic minimum domains

    """
    if not isinstance(atoms, Atoms):
        raise TypeError('atoms must be a Atoms object')
    if not isinstance(periodicity, str) or len(periodicity) != 3:
        raise TypeError('periodicity must be a string of form "pp?"')

    # atoms = atoms.copy()
    # atoms.wrap() # user should use these externally first

    ## Setup fractional conversions and domain sizes
    box = atoms.box
    h, h_inv, boxlo, boxhi = box.get_transformation_matrix()
    lx, ly, lz = box.get_lengths()

    nx = int(lx // cutoff)  # number of domains
    ny = int(ly // cutoff)
    nz = int(lz // cutoff)

    ## number of domains for skewed triclinic, needs testing and 3D checks
    # nx = int(lx // (cutoff / math.cos(math.atan(box.xy / ly)) / math.cos(math.atan(box.xz / lz))))
    # ny = int(ly // (cutoff / math.cos(math.atan(box.yz / lz))))
    # nz = int(lz // cutoff)

    if nx < 3 and periodicity[0] == 'p':
        raise Exception(f'cutoff {cutoff} is too large for box x {lx} to create 3 periodic domains in the x direction')
    if ny < 3 and periodicity[1] == 'p':
        raise Exception(f'cutoff {cutoff} is too large for box y {ly} to create 3 periodic domains in the y direction')
    if nz < 3 and periodicity[2] == 'p':
        raise Exception(f'cutoff {cutoff} is too large for box z {lz} to create 3 periodic domains in the z direction')

    fx = 1 / nx  # use floor div later to get domain index
    fy = 1 / ny
    fz = 1 / nz

    ## fractionalize atoms and assign to domains
    fractionals = {}
    domains = defaultdict(Domain)

    for id_, atom in atoms.items():
        if whitelist is not None and id_ in whitelist:
            pass
        elif blacklist is not None and id_ in blacklist:
            continue

        frac = box.pos2frac(atom.x, atom.y, atom.z, h_inv, boxlo)
        fractionals[id_] = frac
        dx = int(frac[0] // fx)  # box index [0,nx) exclusive if wrapped correctly
        dy = int(frac[1] // fy)
        dz = int(frac[2] // fz)
        box_index = (dx, dy, dz)
        if min(box_index) < 0 or dx >= nx or dy >= ny or dz >= nz:
            raise Exception('Domain index is out of bounds, use Atoms.wrap() before computation')

        domains[box_index].append(id_)  # this is the only problem spot if parallelized

    # self+13 neighboring domains. down, east, south priority ordering.
    neighbor_shifts = [(0, 0, 0), (0, 0, -1), (0, -1, 0), (0, -1, -1), (-1, 0, 0), (-1, 0, -1), (-1, -1, 0),
                       (-1, -1, -1), (-1, 1, 0), (-1, 1, -1), (0, 1, -1), (1, 1, -1), (1, 0, -1), (1, -1, -1)]

    for box_index, domain in domains.items():
        # not sure about use case for these, but these are the lower corner positions
        domain.x, domain.y, domain.z = box.frac2pos(box_index[0] / nx, box_index[1] / ny, box_index[2] / nz, h, boxlo)

        ## Setup neighbor domains to loop through
        for neighbor_shift in neighbor_shifts:
            neighbor_index = []
            image_shift = []
            ## loop directions
            for self_i, shift_i, n_i, period_i in zip(box_index, neighbor_shift, (nx, ny, nz), periodicity):
                shifted = self_i + shift_i
                if shifted >= 0 and shifted < n_i:  # middle of box or looking in
                    neighbor_index.append(shifted)
                    image_shift.append(0)

                elif period_i != 'p':
                    break  # non-periodic, so this neighbor is skipped

                elif shifted < 0:
                    neighbor_index.append(n_i - 1)  # go to top
                    image_shift.append(1)  # add 1 box length in this direction when comparing

                elif shifted >= n_i:
                    neighbor_index.append(0)  # go to bottom
                    image_shift.append(-1)  # subtract 1 box length
                else:
                    raise Exception(f'Something went wrong, this should be unreachable')

            else:  # Skipped by break if non-periodic
                neighbor_index = tuple(neighbor_index)
                if neighbor_index in domains:  # skip empty domains later, faster for sparse boxes
                    # save to this domain neighbors
                    domain.neighbors[neighbor_index] = tuple(image_shift)

    return domains, fractionals
