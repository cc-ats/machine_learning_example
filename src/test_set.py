import os
import sys
import numpy

from deepmd import DeepEval
from deepmd import DeepPot

from utils import hartree_to_ev, bohr_to_angstrom

def l2err (diff) :    
    return numpy.sqrt(numpy.average (diff*diff))

def save_txt_file(fname, data, header = "", append = False):
    fp = fname
    if append : fp = open(fp, 'ab')
    numpy.savetxt(fp, data, header = header)
    if append : fp.close()

class TestSet(object):
    def __init__(self, model_file=None, coord_file=None, energy_file=None, force_file=None, box_file=None, atom_types=None, length_unit="A", energy_unit="Eh", is_pbc=False, verbose=True):
        self.is_pbc     = is_pbc
        self.verbose    = verbose

        if isinstance(atom_types, str):
            self._atm_type = numpy.loadtxt(atom_types, dtype=int)
        else:
            self._atm_type = numpy.asarray(atom_types, dtype=int)

        self.model_file   = model_file
        model_type        = DeepEval(model_file).model_type
        assert model_type == 'ener'
        self.dp           = DeepPot(model_file)

        length_unit = length_unit.lower()
        if length_unit in ["a", "angstrom"]:
            length_unit = "A"
            length_unit_converter = 1.0
        elif length_unit in ["au", "a.u.", "bohr"]:
            length_unit = "Bohr"
            length_unit_converter = bohr_to_angstrom
        else:
            raise AssertionError("Wrong Length Unit")

        energy_unit = energy_unit.lower()
        if energy_unit in ["ev"]:
            energy_unit = "eV"
            energy_unit_converter = 1.0/hartree_to_ev
        elif energy_unit in ["au", "a.u.", "hartree", "eh"]:
            energy_unit = "Eh"
            energy_unit_converter = 1.0
        else:
            raise AssertionError("Wrong Energy Unit")

        self._coord_data  = numpy.load(coord_file)  * length_unit_converter
        self._energy_data = numpy.load(energy_file) * energy_unit_converter
        self._force_data  = numpy.load(force_file)  * energy_unit_converter/length_unit_converter

        self.nframe = self._coord_data.shape[0]
        self.natom  = self._coord_data.shape[1]
        self._atm_type.reshape(self.natom)

        if not is_pbc and (box_file is None):
            self._box_data  = numpy.zeros([self.nframe, 9])
        else:
            self._box_data  = numpy.load(box_file) * length_unit_converter
        
        assert self._box_data.shape    == (self.nframe, 9)
        assert self._coord_data.shape  == (self.nframe, self.natom, 3)
        assert self._force_data.shape  == (self.nframe, self.natom, 3)
        assert self._energy_data.shape == (self.nframe,)
        assert self._atm_type.shape    == (self.natom,)

        self.dump_info(model_file=model_file, atom_types=atom_types,coord_file=coord_file, energy_file=energy_file, force_file=force_file, is_pbc=is_pbc, box_file=box_file, length_unit=length_unit, energy_unit=energy_unit)

    def dump_info(self, **kwargs):
        if not self.verbose:
            return

        if ("model_file" in kwargs) and ("coord_file" in kwargs) and ("energy_file" in kwargs) and ("force_file" in kwargs) and ("box_file" in kwargs) and ("is_pbc" in kwargs) and ("atom_types" in kwargs):
            print ("# ---------------Test data from files:--------------- ")
            print("model_file  = %s"%kwargs["model_file"])
            print("coord_file  = %s"%kwargs["coord_file"])
            print("energy_file = %s"%kwargs["energy_file"])
            print("force_file  = %s"%kwargs["force_file"])
            print("box_file    = %s"%kwargs["box_file"])
            print("# Using periodic boundary condition")

            if kwargs["is_pbc"]:
                print("# Using periodic boundary condition")
            else:
                print("# Not using periodic boundary condition")

            if isinstance(kwargs["atom_types"], str):
                print("# Atom types are given by text file") 
                print("atom_types    = %s"%kwargs["atom_types"])
            else:
                print("# Atom types are given by")
                print(type(kwargs["atom_types"]))
            print ("# -------------------------------------------------- \n")

        if ("length_unit" in kwargs) and ("energy_unit" in kwargs):
            print ("# ---------------Units:--------------- ")
            print("length_unit  = %s"%kwargs["length_unit"])
            print("energy_unit  = %s"%kwargs["energy_unit"])
            print ("# ------------------------------------ \n")

        if ("dir_name" in kwargs) and ("num_set" in kwargs) and ("num_frame_in_a_set" in kwargs):
            print ("# ---------------Building system:--------------- ")
            print("dir_name           = %s"%kwargs["dir_name"])
            print("num_set            = %s"%kwargs["num_set"])
            print("num_frame_in_a_set = %s"%kwargs["num_frame_in_a_set"])
            print ("# ---------------------------------------------- \n")

    def build(self, detail_file=None):
        numb_test    = self.nframe

        energy_data = self._energy_data[:numb_test].reshape([-1,1])
        force_data  = self._force_data[:numb_test].reshape([numb_test, -1])

        coord = self._coord_data.reshape([numb_test, -1])
        box   = self._box_data.reshape([numb_test, -1])
        if not self.is_pbc:
            box = None
        fparam = None
        aparam = None

        atype  = self._atm_type
        atomic = False

        ret = self.dp.eval(coord, box, atype, fparam = fparam, aparam = aparam, atomic = atomic)

        energy = ret[0]
        force  = ret[1]
        virial = ret[2]
        energy = energy.reshape([numb_test,1])
        force  = force.reshape([numb_test,-1])
        virial = virial.reshape([numb_test,9])
        if atomic:
            ae = ret[3]
            av = ret[4]
            ae = ae.reshape([numb_test,-1])
            av = av.reshape([numb_test,-1])

        print("energy - energy_data = ", energy - energy_data)
        l2e = (l2err (energy - energy_data))
        l2f = (l2err (force  - force_data))
        l2ea= l2e/self.natom

        # print ("# energies: %s" % energy)
        print ("# number of test data : %d " % numb_test)
        print ("Energy L2err        : %e eV" % l2e)
        print ("Energy L2err/Natoms : %e eV" % l2ea)
        print ("Force  L2err        : %e eV/A" % l2f)

        if detail_file is not None :

            save_txt_file(detail_file+".c.out", coord,
                        header = 'data_c',
                        append = False)

            pe = numpy.concatenate(
                (
                    numpy.reshape(energy_data,      [numb_test,-1]),
                    numpy.reshape(energy,           [numb_test,-1])
                ), 
                axis = 1
                )
            save_txt_file(detail_file+".e.out", pe,
                        header = 'data_e pred_e',
                        append = False)

            pf = numpy.concatenate(
                (
                    numpy.reshape(force_data,      [numb_test,-1]),
                    numpy.reshape(force,           [numb_test,-1])
                ), 
                axis = 1
                )
            save_txt_file(detail_file+".f.out", pf,
                        header = 'data_f pred_f',
                        append = False)
