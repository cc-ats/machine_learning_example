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
sbatch train_cpu.sh;

python script/test_model.py .;