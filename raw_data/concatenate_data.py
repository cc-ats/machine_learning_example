import numpy
from numpy import load

for xx in ["coord", "energy", "force"]:
    x1 = load("sqm_%s_reactant.npy"%xx)
    x2 = load("sqm_%s_ts.npy"%xx)
    x = concatenate((x1, x2))
    numpy.save("%s.npy"%xx, x)
