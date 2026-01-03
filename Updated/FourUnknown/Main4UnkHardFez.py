import sys
import numpy as np
import math
import qiskit as qk
import QAlgs as qa
from qiskit.quantum_info import Operator
import MatrixProcedures as mp
from qiskit import *
from qiskit.circuit.library import HGate, XGate, RYGate, SwapGate, ZGate, SGate, CZGate
from qiskit.circuit.library import Initialize
from qiskit import QuantumCircuit, qasm2 
from qiskit_aer import AerSimulator


from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_aer.noise import (
    NoiseModel)
service = QiskitRuntimeService()
back1 = service.backend("ibm_fez")
noise_model = NoiseModel.from_backend(back1)
print(
    f"Name: {back1.name}\n"
    f"Version: {back1.version}\n"
    f"No. of qubits: {back1.num_qubits}\n"
    f"basis gates: {back1.basis_gates}"
)


EPSILON=1e-10
shots=1024

# the choice of nq_phase affects the accuracy of QPE
nq_phase=2

# initialize the matrix equation, and prepare it for the quantum procedure
print("Building system... ",end='')
sys.stdout.flush()
msystem = mp.MatrixSystem(M=4,expand=False)
msystem.FileInit()
msystem.PrepSystem()
print("Done.")

# calculate C
C = 1.9999999998

######################################################################################################

# initialize the quantum system itself
reg_phase=qk.QuantumRegister(nq_phase,"phase")
reg_r1=qk.QuantumRegister(msystem.n,"r1")
reg_r1a=qk.QuantumRegister(1,"r1a")
reg_r2=qk.QuantumRegister(msystem.n,"r2")
reg_r2a=qk.QuantumRegister(1, "r2a")
reg_a_hhl=qk.QuantumRegister(1, "a_hhl")
reg_class=qk.ClassicalRegister(nq_phase+2*msystem.n+3)
circ_init = qk.QuantumCircuit(
    reg_a_hhl,
    reg_r2a,
    reg_r2,
    reg_r1a,
    reg_r1,
    reg_phase,
    name="HHL_main",
)
# initial r1 to b

circ_init.barrier()

# initial T
for q in reg_r2:
    circ_init.h(q)
circ_init.barrier()

# QPE
    #Hadamard on phase registers
for q in reg_phase:
    circ_init.h(q)
for i in range(2):
        for j in range(i+1):
            # Bj dagger
            circ_init.append(HGate().control(2,None,'01'),[reg_phase[i]]+[reg_r1a[0]]+[reg_r2[0]])
            circ_init.append(HGate().control(2,None,'01'),[reg_phase[i]]+[reg_r1a[0]]+[reg_r2[1]])
            # Bj' dagger
            circ_init.append(XGate().control(2,None,'11'),[reg_phase[i]]+[reg_r1a[0]]+[reg_r2a[0]])
            #reflection about |0>
            circ_init.append(ZGate().control(1,None,'1'),[reg_phase[i]]+[reg_r2[0]])
            circ_init.append(XGate().control(1,None,'1'),[reg_phase[i]]+[reg_r2[0]])
            circ_init.append(ZGate().control(1,None,'1'),[reg_phase[i]]+[reg_r2[0]])
            circ_init.append(XGate().control(1,None,'1'),[reg_phase[i]]+[reg_r2[0]])

            circ_init.append(XGate().control(3,None,'001'),[reg_phase[i]]+[reg_r2[0]]+[reg_r2[1]]+reg_r2a[:])
            circ_init.append(ZGate().control(3,None,'001'),[reg_phase[i]]+[reg_r2[0]]+[reg_r2[1]]+reg_r2a[:])
            circ_init.append(XGate().control(3,None,'001'),[reg_phase[i]]+[reg_r2[0]]+[reg_r2[1]]+reg_r2a[:])

            circ_init.append(HGate().control(2,None,'01'),[reg_phase[i]]+[reg_r1a[0]]+[reg_r2[0]])
            circ_init.append(HGate().control(2,None,'01'),[reg_phase[i]]+[reg_r1a[0]]+[reg_r2[1]])
            circ_init.append(XGate().control(2,None,'11'),[reg_phase[i]]+[reg_r1a[0]]+[reg_r2a[0]])
            #S
            circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[i]]+[reg_r1[0]]+[reg_r2[0]])
            circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[i]]+[reg_r1[1]]+[reg_r2[1]])
            circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[i]]+reg_r1a[:]+reg_r2a[:])
            # -iI
            circ_init.append(SGate().control(1,None,'1'),[reg_phase[i]]+[reg_r1[0]])
            circ_init.append(XGate().control(1,None,'1'),[reg_phase[i]]+[reg_r1[0]])
            circ_init.append(SGate().control(1,None,'1'),[reg_phase[i]]+[reg_r1[0]])
            circ_init.append(XGate().control(1,None,'1'),[reg_phase[i]]+[reg_r1[0]])
# QFT dagger
circ_init.append(SwapGate(),reg_phase)
circ_init.append(HGate(),[reg_phase[0]])
circ_init.append(CZGate().power(0.5).inverse(),reg_phase)
circ_init.append(HGate(),[reg_phase[1]])
circ_init.barrier()

# HHL ancilla rotation
lam=-msystem.d
circ_init.append(RYGate(2.0*math.acos(C/lam)).control(nq_phase,None,'00'), reg_phase[:]+reg_a_hhl[:])
lam=msystem.X-msystem.d
circ_init.append(RYGate(2.0*math.acos(C/lam)).control(nq_phase,None,'01'), reg_phase[:]+reg_a_hhl[:])
lam=-msystem.d
circ_init.append(RYGate(2.0*math.acos(C/lam)).control(nq_phase,None,'10'), reg_phase[:]+reg_a_hhl[:])
lam=-msystem.X-msystem.d
circ_init.append(RYGate(2.0*math.acos(C/lam)).control(nq_phase,None,'11'), reg_phase[:]+reg_a_hhl[:])
circ_init.barrier()

#inverse QPE
#QFT
circ_init.append(HGate(),[reg_phase[1]])
circ_init.append(CZGate().power(0.5),reg_phase)
circ_init.append(HGate(),[reg_phase[0]])
circ_init.append(SwapGate(),reg_phase)
#walk dagger
for i in [1, 0]:
        for j in range(i+1):
            # -iI
            circ_init.append(XGate().control(1,None,'1'),[reg_phase[i]]+[reg_r1[0]])
            circ_init.append(SGate().inverse().control(1,None,'1'),[reg_phase[i]]+[reg_r1[0]])
            circ_init.append(XGate().control(1,None,'1'),[reg_phase[i]]+[reg_r1[0]])
            circ_init.append(SGate().inverse().control(1,None,'1'),[reg_phase[i]]+[reg_r1[0]])
            # S
            circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[i]]+reg_r1a[:]+reg_r2a[:])
            circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[i]]+[reg_r1[1]]+[reg_r2[1]])
            circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[i]]+[reg_r1[0]]+[reg_r2[0]])
            # reflection about |0>
            circ_init.append(XGate().control(2,None,'11'),[reg_phase[i]]+[reg_r1a[0]]+[reg_r2a[0]])
            circ_init.append(HGate().control(2,None,'01'),[reg_phase[i]]+[reg_r1a[0]]+[reg_r2[1]])
            circ_init.append(HGate().control(2,None,'01'),[reg_phase[i]]+[reg_r1a[0]]+[reg_r2[0]])

            circ_init.append(XGate().control(3,None,'001'),[reg_phase[i]]+[reg_r2[0]]+[reg_r2[1]]+reg_r2a[:])
            circ_init.append(ZGate().control(3,None,'001'),[reg_phase[i]]+[reg_r2[0]]+[reg_r2[1]]+reg_r2a[:])
            circ_init.append(XGate().control(3,None,'001'),[reg_phase[i]]+[reg_r2[0]]+[reg_r2[1]]+reg_r2a[:])

            circ_init.append(XGate().control(1,None,'1'),[reg_phase[i]]+[reg_r2[0]])
            circ_init.append(ZGate().control(1,None,'1'),[reg_phase[i]]+[reg_r2[0]])
            circ_init.append(XGate().control(1,None,'1'),[reg_phase[i]]+[reg_r2[0]])
            circ_init.append(ZGate().control(1,None,'1'),[reg_phase[i]]+[reg_r2[0]])
            # Bj' dagger
            circ_init.append(XGate().control(2,None,'11'),[reg_phase[i]]+[reg_r1a[0]]+[reg_r2a[0]])
            # Bj dagger
            circ_init.append(HGate().control(2,None,'01'),[reg_phase[i]]+[reg_r1a[0]]+[reg_r2[1]])
            circ_init.append(HGate().control(2,None,'01'),[reg_phase[i]]+[reg_r1a[0]]+[reg_r2[0]])

# Un hadamard phase gates:
for q in reg_phase:
    circ_init.h(q)
circ_init.barrier()
#uncompute T
for q in reg_r2:
    circ_init.h(q)
circ_init.barrier()

#########################################################

circ_init.measure_all()

print("Finished building circuit.")
print("Size of logical circuit: ", circ_init.size())
# transpile the circuit
print()
print("Transpiling... ", end="")
sys.stdout.flush()
circ_transpiled = qk.transpile(circ_init, back1, optimization_level=2)
print("Done.")
sys.stdout.flush()
print("Size of transpiled circuit: ", circ_transpiled.size())

sim_noise = AerSimulator(noise_model=noise_model)
 
# Transpile circuit for noisy basis gates
passmanager = generate_preset_pass_manager(
    optimization_level=2, backend=sim_noise
)
circ_tnoise = passmanager.run(circ_init)
 
# Run and get counts
result_bit_flip = sim_noise.run(circ_tnoise, shots=1024).result()
counts_bit_flip = result_bit_flip.get_counts(0)
 
sorted_result = dict(sorted(counts_bit_flip.items(), key=lambda x: x[1], reverse=True))

print(f"res: {sorted_result}")
