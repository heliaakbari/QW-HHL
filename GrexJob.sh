#reference: https://um-grex.github.io/grex-docs/specific-soft/jupyter-notebook/
# first load all the required modules.
module load CCEnv
module load arch/avx512
module load StdEnv/2023 openmpi/5.0.8

#python
module load python/3.13.2 scipy-stack/
which python
#code clone
git clone https://github.com/heliaakbari/QMES.git
git checkout Helia1
cd QMES

# now we can create a virtualenv, install required modules off CCENv wheelhouse
virtualenv venv
source venv/bin/activate
pip install --upgrade pip
pip install qiskit
pip install cirq
pip install numpy
pip install qiskit-aer
pip install psutil #for specs

Python Updated/MainSim.py

#sbatch GrexJob.sh --ntasks=1 --nodes=1 --cpus-per-task=12 --mem=20G --time=0-20:00 --partition=