import sys
sys.path.append("./src/")

from raw_data import RawData

def main(path_prefix, num_set):
    if path_prefix[-1] == "/":
        path_prefix = path_prefix[:-1]

    coord_file    = "%s/raw_data/coord.npy"%path_prefix
    energy_file   = "%s/raw_data/energy.npy"%path_prefix
    force_file    = "%s/raw_data/force.npy"%path_prefix
    atm_type_file = "%s/raw_data/type.raw"%path_prefix

    rd = RawData(
        coord_file  = coord_file,
        energy_file = energy_file,
        force_file  = force_file,
        box_file    = None,
        is_pbc      = False,
        length_unit = "A",
        energy_unit = "Eh",
        atom_types  = atm_type_file,
        verbose     = True
    )
    rd.build(num_set, "%s/data"%path_prefix)

if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
