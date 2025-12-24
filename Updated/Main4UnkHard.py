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
C= 1.99

######################################################################################################
# get the first initializer
init = Initialize(msystem.b).copy(name='Init')

# initialize the quantum system itself
reg_phase=qk.QuantumRegister(nq_phase,"phase")
reg_r1=qk.QuantumRegister(msystem.n,"r1")
reg_r1w=qk.QuantumRegister(max(1, msystem.n - 1),"r1w")
reg_r1a=qk.QuantumRegister(1,"r1a")
reg_r2=qk.QuantumRegister(msystem.n,"r2")
reg_r2w=qk.QuantumRegister(max(1, msystem.n - 1), "r2w")
reg_r2a=qk.QuantumRegister(1, "r2a")
reg_a_hhl=qk.QuantumRegister(1, "a_hhl")
reg_class=qk.ClassicalRegister(nq_phase+2*msystem.n+3)
circ_init = qk.QuantumCircuit(
    reg_a_hhl,
    reg_r2a,
    reg_r2w,
    reg_r2,
    reg_r1a,
    reg_r1w,
    reg_r1,
    reg_phase,
    name="HHL_main",
)
# initial r1 to b
for q in reg_r1:
    circ_init.x(q)

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
            circ_init.append(HGate().control(2,None,'01'),[reg_phase[i]]+[reg_r1a[0]]+[reg_r2[0]])
            circ_init.append(HGate().control(2,None,'01'),[reg_phase[i]]+[reg_r1a[0]]+[reg_r2[1]])
            circ_init.append(XGate().control(2,None,'11'),[reg_phase[i]]+[reg_r1a[0]]+[reg_r2a[0]])

            circ_init.append(ZGate().control(1,None,'1'),[reg_phase[i]]+[reg_r2[0]])
            circ_init.append(XGate().control(1,None,'1'),[reg_phase[i]]+[reg_r2[0]])
            circ_init.append(ZGate().control(1,None,'1'),[reg_phase[i]]+[reg_r2[0]])
            circ_init.append(XGate().control(1,None,'1'),[reg_phase[i]]+[reg_r2[0]])

            circ_init.append(ZGate().control(1,None,'1'),[reg_phase[i]]+[reg_r2[1]])
            circ_init.append(XGate().control(1,None,'1'),[reg_phase[i]]+[reg_r2[1]])
            circ_init.append(ZGate().control(1,None,'1'),[reg_phase[i]]+[reg_r2[1]])
            circ_init.append(XGate().control(1,None,'1'),[reg_phase[i]]+[reg_r2[1]])

            circ_init.append(XGate().control(2,None,'01'),[reg_phase[i]]+[reg_r2[0]]+reg_r2a[:])
            circ_init.append(ZGate().control(2,None,'01'),[reg_phase[i]]+[reg_r2[0]]+reg_r2a[:])
            circ_init.append(XGate().control(2,None,'01'),[reg_phase[i]]+[reg_r2[0]]+reg_r2a[:])

            circ_init.append(XGate().control(2,None,'01'),[reg_phase[i]]+[reg_r2[1]]+reg_r2a[:])
            circ_init.append(ZGate().control(2,None,'01'),[reg_phase[i]]+[reg_r2[1]]+reg_r2a[:])
            circ_init.append(XGate().control(2,None,'01'),[reg_phase[i]]+[reg_r2[1]]+reg_r2a[:])

            circ_init.append(HGate().control(2,None,'01'),[reg_phase[i]]+[reg_r1a[0]]+[reg_r2[0]])
            circ_init.append(HGate().control(2,None,'01'),[reg_phase[i]]+[reg_r1a[0]]+[reg_r2[1]])
            circ_init.append(XGate().control(2,None,'11'),[reg_phase[i]]+[reg_r1a[0]]+[reg_r2a[0]])

            circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[i]]+[reg_r1[0]]+[reg_r2[0]])
            circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[i]]+[reg_r1[1]]+[reg_r2[1]])
            circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[i]]+reg_r1a[:]+reg_r2a[:])

            circ_init.append(SGate().control(1,None,'1'),[reg_phase[i]]+[reg_r1[0]])
            circ_init.append(XGate().control(1,None,'1'),[reg_phase[i]]+[reg_r1[0]])
            circ_init.append(SGate().control(1,None,'1'),[reg_phase[i]]+[reg_r1[0]])
            circ_init.append(XGate().control(1,None,'1'),[reg_phase[i]]+[reg_r1[0]])

circ_init.append(SwapGate(),reg_phase)
circ_init.append(HGate(),[reg_phase[0]])
circ_init.append(CZGate().power(0.5).inverse(),reg_phase)
circ_init.append(HGate(),[reg_phase[1]])
circ_init.barrier()

latex_code = circ_init.draw(
    output="latex_source",
    fold=25   # try 20–40
)
with open("circuit.tex", "w") as f:
    f.write(latex_code)


#result
back1 = AerSimulator(method="statevector")
#print(circ_init.draw(output="text"))

print("Finished building circuit.")
print("Size of logical circuit: ", circ_init.size())
# transpile the circuit
print()
print("Transpiling... ", end="")
sys.stdout.flush()
circ_transpiled = qk.transpile(circ_init, back1, optimization_level=3)
print("Done.")
sys.stdout.flush()
print("Size of transpiled circuit: ", circ_transpiled.size())

circ_transpiled.save_statevector()
# run the circuit and extract results
print()
print("Running circuit... ", end="")
sys.stdout.flush()

# Run the transpiled circuit on the AerSimulator
job = back1.run(circ_transpiled)
result = job.result()

# get the final statevector
# get_statevector requires the circuit reference; passing circ_transpiled is robust
try:
    statevector = result.get_statevector(circ_transpiled)
except Exception:
    # fallback: if only one circuit was executed, get_statevector() without args may work
    statevector = result.get_statevector()

#qa.PrintStatevector(statevector, nq_phase, msystem)

# process the results: extract the solution and compare with a classical solution
# can also check QPE by removing Rc and QPE inverses in the main circuit, and uncommenting below
qa.PrintStatevector(statevector,nq_phase,msystem)
#qa.CheckQPE(statevector, nq_phase, msystem)
sol = qa.ExtractSolution(statevector, nq_phase, msystem)
msystem.CompareClassical(sol)

print()
print(f"circuit size: {circ_transpiled.size()}")

