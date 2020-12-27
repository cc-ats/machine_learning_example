import sys
import os
import shutil
import uuid
import subprocess as sp
from multiprocessing import Pool

import numpy as np


qc_rem = """\
$rem
JOBTYPE force
SYMMETRY false
SYM_IGNORE true
QM_MM true
BASIS 6-31G*
SCF_CONVERGENCE 7
METHOD B3LYP
SKIP_CHARGE_SELF_INTERACT true
$end
"""


ELEMENTS = ["None", 'H', 'He',
            'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
            'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar',
            'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
            'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe',
            'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb',
            'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi']


def get_element_symbols(atomic_number):
    try:
        return [ELEMENTS[i] for i in atomic_number]
    except TypeError:
        return ELEMENTS[atomic_number]


def get_qchem_input(qc_inp, qm_pos, qm_elem_num, charge, mult):
    assert len(qm_pos) == len(qm_elem_num)
    qm_element = get_element_symbols(qm_elem_num)
    with open(qc_inp, 'w') as f:
        f.write("$molecule\n")
        f.write("%d %d\n" % (charge, mult))
        for i in range(len(qm_pos)):
            f.write("".join(["%-3s" % qm_element[i],
                             "%25.16f" % qm_pos[i, 0],
                             "%25.16f" % qm_pos[i, 1],
                             "%25.16f" % qm_pos[i, 2], "\n"]))
        f.write("$end" + "\n\n")

        f.write("$external_charges\n")
        f.write("$end\n\n")

        f.write(qc_rem + "\n")


def get_qchem_force(qm_pos, qm_elem_num, charge, mult):
    cwd = "/dev/shm/run_" + str(uuid.uuid4())
    if not os.path.exists(cwd):
        os.mkdir(cwd)
    get_qchem_input(cwd + "/qchem.inp", qm_pos, qm_elem_num, charge, mult)

    cmdline = f"cd {cwd}; "
    cmdline += f"QCSCRATCH={cwd} qchem qchem.inp qchem.out save > qchem_run.log"
    proc = sp.Popen(args=cmdline, shell=True)
    proc.wait()

    force = np.fromfile(cwd + "/save/131.0", dtype="f8").reshape(-1, 3)
    energy = np.fromfile(cwd + "/save/99.0", dtype="f8", count=2)[1]

    shutil.rmtree(cwd)

    return force, energy


def get_qchem_training_set(coords, qm_elem_num, charge, mult):
    args = ((qm_pos, qm_elem_num, charge, mult) for qm_pos in coords)
    with Pool() as p:
        res = p.starmap(get_qchem_force, args)
    forces = []
    energies = []
    for r in res:
        forces.append(r[0])
        energies.append(r[1])
    forces = np.array(forces)
    energies = np.array(energies)

    return forces, energies
