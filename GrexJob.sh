#!/bin/bash
#SBATCH  --ntasks=1
#SBATCH  --nodes=1
#SBATCH  --cpus-per-task=12
#SBATCH  --mem=20G
#SBATCH  --time=0-20:00
#SBATCH   --partition=

module load CCEnv
module load arch/avx512
module load StdEnv/2023 openmpi/5.0.8


module load python/3.13.2 scipy-stack/
which python

git clone https://github.com/heliaakbari/QMES.git
git checkout Helia1
cd QMES

virtualenv venv
source venv/bin/activate
pip install --upgrade pip
pip install qiskit
pip install cirq
pip install numpy
pip install qiskit-aer
pip install psutil

Python Updated/MainSim.py
