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
# module load CUDA/10.1.243-GCC-8.3.0;
module load deepmd-kit/1.2.1-foss-2020a;
export OMP_NUM_THREADS=20

rm -rf ./train/;
rm -rf ./data/;
rm -rf ./test/;

mkdir train;
python script/build_system.py . 10;

mkdir data;
cd train;
cp ../src/inp_se_ar.json ./inp.json;
dp train                   inp.json;
dp freeze -o               model.pb;

cd ..;
mkdir test;
python script/test_model.py      .;

module purge;
python script/plot.py            .;
