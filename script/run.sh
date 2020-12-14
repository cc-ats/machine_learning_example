#!/bin/bash
#SBATCH --partition=normal
#SBATCH --exclusive
#SBATCH --ntasks=20
#SBATCH --ntasks-per-node=20
#SBATCH --output=%j.out
#SBATCH --error=%j.err
#SBATCH --time=20:00:00
#SBATCH --job-name=test

module purge;
module load deepmd-kit/1.2.1-foss-2020a;
export OMP_NUM_THREADS=20

rm -rf ./train/;
mkdir train;
rm -rf ./data/;
mkdir data;
rm -rf ./test/;
mkdir test;

python script/build_system.py . 4;

cd train;
cp ../src/inp.json     .;
cp ../src/train_cpu.sh .;

dp train     inp.json
dp freeze -o model.pb

cd ..;
python script/test_model.py .;
