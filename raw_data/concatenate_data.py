import numpy
from numpy import load, concatenate

for xx in ["coord", "energy", "force"]:
    if xx != "coord":
        x1 = load("sqm_%s_reactant.npy"%xx)
        x2 = load("sqm_%s_ts.npy"%xx)
    elif xx == "coord":
        x1 = load("%s_reactant.npy"%xx)
        x2 = load("%s_ts.npy"%xx)
    x = concatenate((x1, x2))
    numpy.save("%s.npy"%xx, x)
