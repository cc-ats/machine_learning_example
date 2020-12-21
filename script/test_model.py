import sys
sys.path.append("./src/")

from test_set import TestSet

def main(path_prefix):
    if path_prefix[-1] == "/":
        path_prefix = path_prefix[:-1]

    coord_file    = "%s/raw_data/coord.npy"%path_prefix
    energy_file   = "%s/raw_data/energy.npy"%path_prefix
    force_file    = "%s/raw_data/force.npy"%path_prefix
    atm_type_file = "%s/raw_data/type.raw"%path_prefix
    model_file    = "%s/train/model.pb"%path_prefix
    detail_file   = "%s/test/test"%path_prefix

    ts = TestSet(
        model_file  = model_file,
        coord_file  = coord_file,
        energy_file = energy_file,
        force_file  = force_file,
        box_file    = None,
        is_pbc      = False,
        length_unit = "A",
        energy_unit = "Eh",
        force_unit  = "Eh/Bohr",
        atom_types  = atm_type_file,
        verbose     = True
    )
    ts.build(detail_file=detail_file)

if __name__ == "__main__":
    main(sys.argv[1])
