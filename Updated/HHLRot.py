import sys
import math
import qiskit as qk
import MatrixProcedures as mp
import QAlgs as qa
import QWOps as qw
from qiskit import *
from qiskit.circuit.library import HGate, XGate, RYGate, SwapGate, ZGate, SGate, CZGate
from qiskit.circuit.library import Initialize
from qiskit_aer import AerSimulator

EPSILON=1e-10
shots=4096
start_op=80
stop_op=130

back1 = AerSimulator(method="statevector")
if(start_op==0):
    f = open('./job_data.dat', 'w')
else:
    f = open('./job_data.dat', 'a')

# the choice of nq_phase affects the accuracy of QPE
nq_phase=2

# initialize the matrix equation, and prepare it for the quantum procedure
print("Building system... ",end='')
sys.stdout.flush()
msystem = mp.MatrixSystem(M=2,expand=False)
msystem.FullyQuantumInit()
print("Done.")

# calculate C
C=0.9999999998

# get the first initializer
init = Initialize(msystem.b).copy(name='Init')

# initialize the quantum system itself
reg_phase=qk.QuantumRegister(nq_phase,"p")
reg_a_hhl=qk.QuantumRegister(1, "a")
reg_class=qk.ClassicalRegister(nq_phase+2*msystem.n+3)


# initial T

circ_init=qk.QuantumCircuit(reg_phase,reg_a_hhl)

# HHL ancilla rotation
lam=-msystem.d
circ_init.append(RYGate(2.0*math.acos(C/lam)).control(nq_phase,None,'00'), reg_phase[:]+reg_a_hhl[:])
lam=msystem.X-msystem.d
circ_init.append(RYGate(2.0*math.acos(C/lam)).control(nq_phase,None,'01'), reg_phase[:]+reg_a_hhl[:])
lam=-msystem.d
circ_init.append(RYGate(2.0*math.acos(C/lam)).control(nq_phase,None,'10'), reg_phase[:]+reg_a_hhl[:])
lam=-msystem.X-msystem.d
circ_init.append(RYGate(2.0*math.acos(C/lam)).control(nq_phase,None,'11'), reg_phase[:]+reg_a_hhl[:])


#result
print(circ_init.draw(output="latex_source"))

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

f.close()

