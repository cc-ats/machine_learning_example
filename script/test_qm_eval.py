from qmmm_eval import  DeepQMMM
from numpy import load, loadtxt

def main():
    atom_types = loadtxt("system/type.raw")
    coord  = load("system/set.000/coord.npy")
    box    = load("system/set.000/box.npy")
    aparam = load("system/set.000/aparam.npy")

    deep_qmmm = DeepQMMM("frozen_model.pb")
    print(deep_qmmm.eval(coord, box, atom_types, fparam = None, aparam = aparam, atomic = True))

if __name__ == '__main__':
    main()