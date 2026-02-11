#!/bin/bash

#SBATCH  --ntasks=1
#SBATCH  --nodes=1
#SBATCH  --cpus-per-task=12
#SBATCH  --mem=20G
#SBATCH  --time=0-20:00
#SBATCH  --partition=genoa

module load arch/avx512 gcc/13.2.0 python/3.12
source ~/my_qiskit_env/bin/activate

for m in 2 4
do
    for p in {1..6}
    do
        for q in {2..3}
        do
            python Updated/MainSim.py ${m} ${p} ${q}
        done
    done
done

deactivate


