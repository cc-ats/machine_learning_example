rm -rf ./train/;
rm -rf ./data/;

python script/build_system.py . 4;
mkdir train;
cd    train;

cp ../src/inp.json     .;
cp ../src/train_cpu.sh .;
sbatch train_cpu.sh;