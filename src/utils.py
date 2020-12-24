bohr_to_angstrom = 0.529177210903
hartree_to_ev    = 27.211386245988

def dump_info(kwargs):
    if ("model_file" in kwargs):
        print ("# ---------------Model from files:--------------- ")
        print("model_file  = %s"%kwargs["model_file"])

    if ("coord_file" in kwargs) and ("energy_file" in kwargs) and ("force_file" in kwargs) and ("grad_file" in kwargs) and ("box_file" in kwargs) and ("is_pbc" in kwargs) and ("atom_types" in kwargs):
        print ("# ---------------Raw data from files:--------------- ")
        print("coord_file  = %s"%kwargs["coord_file"])
        print("energy_file = %s"%kwargs["energy_file"])
        print("force_file  = %s"%kwargs["force_file"])
        print("grad_file   = %s"%kwargs["grad_file"])
        print("box_file    = %s"%kwargs["box_file"])
        
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

    if ("length_unit" in kwargs) and ("energy_unit" in kwargs) and ("force_unit" in kwargs):
        print ("# ---------------Units:--------------- ")
        print("length_unit  = %s"%kwargs["length_unit"])
        print("energy_unit  = %s"%kwargs["energy_unit"])
        print("force_unit   = %s"%kwargs["force_unit"])
        print ("# ------------------------------------ \n")

    if ("dir_name" in kwargs) and ("num_set" in kwargs) and ("num_frame_in_a_set" in kwargs):
        print ("# ---------------Building system:--------------- ")
        print("dir_name           = %s"%kwargs["dir_name"])
        print("num_set            = %s"%kwargs["num_set"])
        print("num_frame_in_a_set = %s"%kwargs["num_frame_in_a_set"])
        print ("# ---------------------------------------------- \n")

def get_length_unit_converter(length_unit):
    length_unit = length_unit.lower()
    if length_unit in ["a", "angstrom"]:
        length_unit_          = "A"
        length_unit_converter = 1.0
    elif length_unit in ["au", "a.u.", "bohr"]:
        length_unit_     = "Bohr"
        length_unit_converter = bohr_to_angstrom
    else:
        print("length_unit = %s"%length_unit)
        raise AssertionError("Wrong Length Unit")

    return length_unit_, length_unit_converter

def get_energy_unit_converter(energy_unit):
    energy_unit = energy_unit.lower()
    if energy_unit in ["ev"]:
        energy_unit_          = "eV"
        energy_unit_converter = 1.0
    elif energy_unit in ["au", "a.u.", "hartree", "eh"]:
        energy_unit_          = "Eh"
        energy_unit_converter = hartree_to_ev
    else:
        print("energy_unit = %s"%energy_unit)
        raise AssertionError("Wrong Energy Unit")

    return energy_unit_, energy_unit_converter