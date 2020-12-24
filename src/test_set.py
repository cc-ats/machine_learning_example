import os
import sys
import numpy

from deepmd import DeepEval
from deepmd import DeepPot

from utils import get_energy_unit_converter, get_length_unit_converter, get_force_unit_converter
from utils import dump_info

def l2err (diff) :    
    return numpy.sqrt(numpy.average (diff*diff))

def save_txt_file(fname, data, header = "", append = False):
    fp = fname
    if append : fp = open(fp, 'ab')
    numpy.savetxt(fp, data, header = header)
    if append : fp.close()

class TestSet(object):
    def __init__(self, model_file=None,
    coord_file=None, energy_file=None, force_file=None, grad_file=None, box_file=None,
    atom_types=None, length_unit="A", energy_unit="Eh", force_unit="Eh/Bohr",
    is_pbc=False, verbose=True):

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

        length_unit, length_unit_converter = get_length_unit_converter(length_unit)
        energy_unit, energy_unit_converter = get_energy_unit_converter(energy_unit)
        force_unit,  force_unit_converter  = get_force_unit_converter(force_unit)

        self._coord_data  = numpy.load(coord_file)   * length_unit_converter
        self._energy_data = numpy.load(energy_file)  * energy_unit_converter
        if force_file is not None and grad_file is None:
            self._force_data  = numpy.load(force_file)  * force_unit_converter
        elif force_file is None and grad_file is not None:
            self._force_data  = - numpy.load(grad_file)  * force_unit_converter

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

        self.dump_info(
            model_file=model_file,
            atom_types=atom_types, is_pbc=is_pbc,
            coord_file=coord_file, energy_file=energy_file,
            force_file=force_file, grad_file=grad_file,
            box_file=box_file,
            length_unit=length_unit,
            energy_unit=energy_unit,
            force_unit=force_unit
            )

    def dump_info(self, **kwargs):
        if not self.verbose:
            return

        dump_info(kwargs)

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

        l2e = (l2err (energy - energy_data))
        l2f = (l2err (force  - force_data))
        l2ea= l2e/self.natom

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