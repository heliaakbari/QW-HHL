#!/bin/bash

#SBATCH  --ntasks=1
#SBATCH  --nodes=1
#SBATCH  --cpus-per-task=12
#SBATCH  --mem=20G
#SBATCH  --time=0-20:00
#SBATCH  --partition=genoa

module load arch/avx512 gcc/13.2.0 python/3.12
source ~/my_qiskit_env/bin/activate

KAPPAS=(4 8 16 32 64 128)

SEEDS=(1 2 3 4)

for seed in "${SEEDS[@]}"; do
    for kappa in "${KAPPAS[@]}"; do
        echo "Running kappa=$kappa seed=$seed"
        python Updated/MainSim.py \
        --mode kappatest \
        --dimension 2 \
        --phase 2 \
        --kappa "$kappa" \
        --seed "$seed"
  done
done

deactivate


