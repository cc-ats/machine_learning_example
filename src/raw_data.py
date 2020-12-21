import numpy
import os, shutil

from utils import get_energy_unit_converter, get_length_unit_converter, get_force_unit_converter
from utils import dump_info

class RawData(object):
    def __init__(self, coord_file=None, energy_file=None, force_file=None, box_file=None, atom_types=None, length_unit="A", energy_unit="Eh", force_unit="Eh/Bohr", is_pbc=False, verbose=True):
        self.is_pbc     = is_pbc
        self.verbose    = verbose

        if isinstance(atom_types, str):
            self._atm_type = numpy.loadtxt(atom_types, dtype=int)
        else:
            self._atm_type = numpy.asarray(atom_types, dtype=int)

        length_unit, length_unit_converter = get_length_unit_converter(length_unit)
        energy_unit, energy_unit_converter = get_energy_unit_converter(energy_unit)
        force_unit,  force_unit_converter  = get_force_unit_converter(force_unit)

        self._coord_data  = numpy.load(coord_file)  * length_unit_converter
        self._energy_data = numpy.load(energy_file) * energy_unit_converter
        self._force_data  = numpy.load(force_file)  * force_unit_converter

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

        self.dump_info(atom_types=atom_types,coord_file=coord_file, energy_file=energy_file, force_file=force_file, is_pbc=is_pbc, box_file=box_file, length_unit=length_unit, energy_unit=energy_unit, force_unit=force_unit)

    def dump_info(self, **kwargs):
        if not self.verbose:
            return

        dump_info(kwargs)

    def build(self, num_set, dir_name):
        assert isinstance(dir_name, str)
        if dir_name[-1] == "/":
            dir_name = dir_name[:-1]

        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.makedirs(dir_name)
        numpy.savetxt("%s/type.raw"%dir_name, self._atm_type, fmt="%d", delimiter=',')
            
        num_frame_in_a_set = self.nframe//num_set
        assert num_frame_in_a_set > 1
        num_frame_in_sys   = num_set * num_frame_in_a_set
        index_labels       = numpy.arange(num_frame_in_sys, dtype=int)
        numpy.random.shuffle(index_labels)
        index_labels       = index_labels.reshape(num_set, num_frame_in_a_set)
        self.dump_info(num_set=num_set, dir_name=dir_name, num_frame_in_a_set=num_frame_in_a_set)

        for i in range(num_set):
            indices = index_labels[i]
            set_name = "set.%03d"%i
            path_name = "%s/%s"%(dir_name, set_name)
            os.makedirs(path_name)
            print("Making %s"%path_name)

            data = self._box_data[indices].reshape(num_frame_in_a_set,9).astype(numpy.float32)
            numpy.save("%s/box"%path_name, data)
            
            data = self._coord_data[indices].reshape(num_frame_in_a_set,-1).astype(numpy.float32)
            numpy.save("%s/coord"%path_name, data)
            
            data = self._energy_data[indices].reshape(num_frame_in_a_set,).astype(numpy.float32)
            numpy.save("%s/energy"%path_name, data)
            
            data = self._force_data[indices].reshape(num_frame_in_a_set,-1).astype(numpy.float32)
            numpy.save("%s/force"%path_name, data)

        if not self.is_pbc:
            path_name = "%s/%s"%(dir_name, "nopbc")
            with open(path_name, "w") as f:
                pass
