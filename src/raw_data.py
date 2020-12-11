import numpy
import os, shutil

from utils import hartree_to_ev, bohr_to_angstrom

class RawData(object):
    def __init__(self, coord_file=None, energy_file=None, force_file=None, box_file=None, atom_types=None, length_unit="A", energy_unit="Eh", is_pbc=False, verbose=True):
        self.is_pbc     = is_pbc
        self.verbose    = verbose

        if isinstance(atom_types, str):
            self._atm_type = numpy.loadtxt(atom_types, dtype=int)
        else:
            self._atm_type = numpy.asarray(atom_types, dtype=int)

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

        self.dump_info(atom_types=atom_types,coord_file=coord_file, energy_file=energy_file, force_file=force_file, is_pbc=is_pbc, box_file=box_file, length_unit=length_unit, energy_unit=energy_unit)

    def dump_info(self, **kwargs):
        if not self.verbose:
            return

        if ("coord_file" in kwargs) and ("energy_file" in kwargs) and ("force_file" in kwargs) and ("box_file" in kwargs) and ("is_pbc" in kwargs) and ("atom_types" in kwargs):
            print("#############################")
            print("Raw data from files:")
            print("coord_file  = %s"%kwargs["coord_file"])
            print("energy_file = %s"%kwargs["energy_file"])
            print("force_file  = %s"%kwargs["force_file"])
            print("box_file    = %s"%kwargs["box_file"])
            print("Using periodic boundary condition")
            if kwargs["is_pbc"]:
                print("Using periodic boundary condition")
            else:
                print("Not using periodic boundary condition") 
            if isinstance(kwargs["atom_types"], str):
                print("Atom types are given by text file") 
                print("atom_types    = %s"%kwargs["atom_types"])
            else:
                print("Atom types are given by")
                print(type(kwargs["atom_types"]))
            print("#############################\n")

        if ("length_unit" in kwargs) and ("energy_unit" in kwargs):
            print("#############################")
            print("Units:")
            print("length_unit  = %s"%kwargs["length_unit"])
            print("energy_unit  = %s"%kwargs["energy_unit"])
            print("#############################\n")

        if ("dir_name" in kwargs) and ("num_set" in kwargs):
            print("#############################")
            print("Building system:")
            print("dir_name     = %s"%kwargs["dir_name"])
            print("num_set      = %s"%kwargs["num_set"])
            print("#############################\n")

    def build_system(self, num_set, dir_name):
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
        self.dump_info(num_set=num_set, dir_name=dir_name)

        for i in range(num_set):
            indices = index_labels[i]
            set_name = "set.%03d"%i
            path_name = "%s/%s"%(dir_name, set_name)
            os.makedirs(path_name)
            
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