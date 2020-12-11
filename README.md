# machine_learning_example
This repository could be copied to `oscer` with `git clone git@github.com:cc-ats/machine_learning_example.git`. It would be more than welcomed to submit any bugs and feature request in the issue section. I also recommend you to set up your own `branch` by,
```
git 
```
## Raw data
This is a machine learning example, we start from the files inside `raw_data`:
```
raw_data:
coord.npy  energy.npy  force.npy
```
The data could be read with `numpy.load`, for example, 
```
python -c '
from numpy import load
coord_data  = load("./raw_data/coord.npy")
force_data  = load("./raw_data/force.npy")
energy_data = load("./raw_data/energy.npy")

print("coord_data.shape  = ",  coord_data.shape)
print("force_data.shape  = ",  force_data.shape)
print("energy_data.shape = ", energy_data.shape)
'
```
we have,
```
coord_data.shape  =  (1000, 96, 3)
force_data.shape  =  (1000, 96, 3)
energy_data.shape =  (1000,)
```
all the energies are in [atomic unit](https://en.wikipedia.org/wiki/Hartree_atomic_units) <a href="https://www.codecogs.com/eqnedit.php?latex=E_\mathrm{h}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E_\mathrm{h}" title="E_\mathrm{h}" /></a>, the coordinates are in  <a href="https://www.codecogs.com/eqnedit.php?latex=\text{\normalfont\AA}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\text{\normalfont\AA}" title="\text{\normalfont\AA}" /></a>, and the forces are in <a href="https://www.codecogs.com/eqnedit.php?latex=E_\mathrm{h}/\text{\normalfont\AA}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E_\mathrm{h}/\text{\normalfont\AA}" title="E_\mathrm{h}/\text{\normalfont\AA}" /></a>. However, the working units of `DeePMD-kit` are, (<a href="https://www.codecogs.com/eqnedit.php?latex=1E_\mathrm{h}&space;=&space;27.211386245988\mathrm{eV}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?1E_\mathrm{h}&space;=&space;27.211386245988\mathrm{eV}" title="1E_\mathrm{h} = 27.211386245988\mathrm{eV}" /></a>)
Property| Unit
---	| :---:
Time	| <a href="https://www.codecogs.com/eqnedit.php?latex=\mathrm{ps}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathrm{ps}" title="\mathrm{ps}" /></a>
Length	| <a href="https://www.codecogs.com/eqnedit.php?latex=\text{\normalfont\AA}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\text{\normalfont\AA}" title="\text{\normalfont\AA}" /></a>
Energy	| <a href="https://www.codecogs.com/eqnedit.php?latex=\mathrm{eV}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathrm{eV}" title="\mathrm{eV}" /></a>
Force	| <a href="https://www.codecogs.com/eqnedit.php?latex=\mathrm{eV}/\text{\normalfont\AA}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathrm{eV}/\text{\normalfont\AA}" title="\mathrm{eV}/\text{\normalfont\AA}" /></a>
Pressure| <a href="https://www.codecogs.com/eqnedit.php?latex=\mathrm{Bar}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mathrm{Bar}" title="\mathrm{Bar}" /></a>

## Build system
We can use `./script/build_system.py` to build the `system`:
```
python script/build_system.py . 4
```

## Train the model
To set up the training
```
mkdir train
cd train
cp ../src/inp.json     .
cp ../src/train_cpu.sh .
sbatch train_cpu.sh
```
please make sure you have carefully read the `inp.json` file and the `train_cpu.sh` before submitting it.

## Summary
You can do all the thing by,
```
bash ./script/run.sh
```