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
shots=4096
start_op=80
stop_op=130

#back1 = AerSimulator(method="statevector")
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
reg_phase=qk.QuantumRegister(nq_phase,"phase")
reg_r1=qk.QuantumRegister(msystem.n,"r1")
#reg_r1w=qk.QuantumRegister(msystem.n,"r1w")
reg_r1a=qk.QuantumRegister(1,"r1a")
reg_r2=qk.QuantumRegister(msystem.n,"r2")
#reg_r2w=qk.QuantumRegister(msystem.n, "r2w")
reg_r2a=qk.QuantumRegister(1, "r2a")
reg_a_hhl=qk.QuantumRegister(1, "a_hhl")
reg_class=qk.ClassicalRegister(nq_phase+2*msystem.n+3)

reg_all=reg_phase[:]+reg_r1[:]+reg_r1a[:]+reg_r2[:]+reg_r2a[:]+reg_a_hhl[:]

# initial T

circ_init=qk.QuantumCircuit(reg_a_hhl, reg_r2a, reg_r2, reg_r1a, reg_r1, reg_phase)
circ_init.append(HGate(), reg_r2)
circ_init.barrier()
# QPE
circ_init.append(HGate(),[reg_phase[0]])
circ_init.append(HGate(),[reg_phase[1]])
circ_init.append(HGate().control(2,None,'01'),[reg_phase[0]]+[reg_r1a[0]]+[reg_r2[0]])
circ_init.append(XGate().control(2,None,'11'),[reg_phase[0]]+[reg_r1a[0]]+[reg_r2a[0]])
circ_init.append(ZGate().control(1,None,'1'),[reg_phase[0]]+[reg_r2[0]])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[0]]+[reg_r2[0]])
circ_init.append(ZGate().control(1,None,'1'),[reg_phase[0]]+[reg_r2[0]])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[0]]+[reg_r2[0]])
circ_init.append(XGate().control(2,None,'01'),[reg_phase[0]]+reg_r2[:]+reg_r2a[:])
circ_init.append(ZGate().control(2,None,'01'),[reg_phase[0]]+reg_r2[:]+reg_r2a[:])
circ_init.append(XGate().control(2,None,'01'),[reg_phase[0]]+reg_r2[:]+reg_r2a[:])
circ_init.append(HGate().control(2,None,'01'),[reg_phase[0]]+[reg_r1a[0]]+[reg_r2[0]])
circ_init.append(XGate().control(2,None,'11'),[reg_phase[0]]+[reg_r1a[0]]+[reg_r2a[0]])
circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[0]]+reg_r1[:]+reg_r2[:])
circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[0]]+reg_r1a[:]+reg_r2a[:])
circ_init.append(SGate().control(1,None,'1'),[reg_phase[0]]+[reg_r1[0]])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[0]]+[reg_r1[0]])
circ_init.append(SGate().control(1,None,'1'),[reg_phase[0]]+[reg_r1[0]])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[0]]+[reg_r1[0]])
circ_init.append(HGate().control(2,None,'01'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2[0]])
circ_init.append(XGate().control(2,None,'11'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2a[0]])
circ_init.append(ZGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
circ_init.append(ZGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
circ_init.append(XGate().control(2,None,'01'),[reg_phase[1]]+reg_r2[:]+reg_r2a[:])
circ_init.append(ZGate().control(2,None,'01'),[reg_phase[1]]+reg_r2[:]+reg_r2a[:])
circ_init.append(XGate().control(2,None,'01'),[reg_phase[1]]+reg_r2[:]+reg_r2a[:])
circ_init.append(HGate().control(2,None,'01'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2[0]])
circ_init.append(XGate().control(2,None,'11'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2a[0]])
circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[1]]+reg_r1[:]+reg_r2[:])
circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[1]]+reg_r1a[:]+reg_r2a[:])
circ_init.append(SGate().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
circ_init.append(SGate().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
circ_init.append(HGate().control(2,None,'01'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2[0]])
circ_init.append(XGate().control(2,None,'11'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2a[0]])
circ_init.append(ZGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
circ_init.append(ZGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
circ_init.append(XGate().control(2,None,'01'),[reg_phase[1]]+reg_r2[:]+reg_r2a[:])
circ_init.append(ZGate().control(2,None,'01'),[reg_phase[1]]+reg_r2[:]+reg_r2a[:])
circ_init.append(XGate().control(2,None,'01'),[reg_phase[1]]+reg_r2[:]+reg_r2a[:])
circ_init.append(HGate().control(2,None,'01'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2[0]])
circ_init.append(XGate().control(2,None,'11'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2a[0]])
circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[1]]+reg_r1[:]+reg_r2[:])
circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[1]]+reg_r1a[:]+reg_r2a[:])
circ_init.append(SGate().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
circ_init.append(SGate().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
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
# inverse QPE
circ_init.append(HGate(),[reg_phase[1]])
circ_init.append(CZGate().power(0.5),reg_phase)
circ_init.append(HGate(),[reg_phase[0]])
circ_init.append(SwapGate(),reg_phase)
circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
circ_init.append(SGate().inverse().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
circ_init.append(SGate().inverse().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[1]]+reg_r1a[:]+reg_r2a[:])
circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[1]]+reg_r1[:]+reg_r2[:])
circ_init.append(XGate().control(2,None,'11'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2a[0]])
circ_init.append(HGate().control(2,None,'01'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2[0]])
circ_init.append(XGate().control(2,None,'01'),[reg_phase[1]]+reg_r2[:]+reg_r2a[:])
circ_init.append(ZGate().control(2,None,'01'),[reg_phase[1]]+reg_r2[:]+reg_r2a[:])
circ_init.append(XGate().control(2,None,'01'),[reg_phase[1]]+reg_r2[:]+reg_r2a[:])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
circ_init.append(ZGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
circ_init.append(ZGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
circ_init.append(XGate().control(2,None,'11'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2a[0]])
circ_init.append(HGate().control(2,None,'01'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2[0]])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
circ_init.append(SGate().inverse().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
circ_init.append(SGate().inverse().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[1]]+reg_r1a[:]+reg_r2a[:])
circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[1]]+reg_r1[:]+reg_r2[:])
circ_init.append(XGate().control(2,None,'11'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2a[0]])
circ_init.append(HGate().control(2,None,'01'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2[0]])
circ_init.append(XGate().control(2,None,'01'),[reg_phase[1]]+reg_r2[:]+reg_r2a[:])
circ_init.append(ZGate().control(2,None,'01'),[reg_phase[1]]+reg_r2[:]+reg_r2a[:])
circ_init.append(XGate().control(2,None,'01'),[reg_phase[1]]+reg_r2[:]+reg_r2a[:])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
circ_init.append(ZGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
circ_init.append(ZGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
circ_init.append(XGate().control(2,None,'11'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2a[0]])
circ_init.append(HGate().control(2,None,'01'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2[0]])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[0]]+[reg_r1[0]])
circ_init.append(SGate().inverse().control(1,None,'1'),[reg_phase[0]]+[reg_r1[0]])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[0]]+[reg_r1[0]])
circ_init.append(SGate().inverse().control(1,None,'1'),[reg_phase[0]]+[reg_r1[0]])
circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[0]]+reg_r1a[:]+reg_r2a[:])
circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[0]]+reg_r1[:]+reg_r2[:])
circ_init.append(XGate().control(2,None,'11'),[reg_phase[0]]+[reg_r1a[0]]+[reg_r2a[0]])
circ_init.append(HGate().control(2,None,'01'),[reg_phase[0]]+[reg_r1a[0]]+[reg_r2[0]])
circ_init.append(XGate().control(2,None,'01'),[reg_phase[0]]+reg_r2[:]+reg_r2a[:])
circ_init.append(ZGate().control(2,None,'01'),[reg_phase[0]]+reg_r2[:]+reg_r2a[:])
circ_init.append(XGate().control(2,None,'01'),[reg_phase[0]]+reg_r2[:]+reg_r2a[:])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[0]]+[reg_r2[0]])
circ_init.append(ZGate().control(1,None,'1'),[reg_phase[0]]+[reg_r2[0]])
circ_init.append(XGate().control(1,None,'1'),[reg_phase[0]]+[reg_r2[0]])
circ_init.append(ZGate().control(1,None,'1'),[reg_phase[0]]+[reg_r2[0]])
circ_init.append(XGate().control(2,None,'11'),[reg_phase[0]]+[reg_r1a[0]]+[reg_r2a[0]])
circ_init.append(HGate().control(2,None,'01'),[reg_phase[0]]+[reg_r1a[0]]+[reg_r2[0]])
circ_init.append(HGate(),[reg_phase[1]])
circ_init.append(HGate(),[reg_phase[0]])
circ_init.barrier()
# inverse T
circ_init.append(HGate(),reg_r2)


circ_init.measure_all()

#result
print(circ_init.draw(output="latex_source"))

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

#circ_transpiled.save_statevector()
# run the circuit and extract results
print()
print("Running circuit... ", end="")
sys.stdout.flush()

# Run the transpiled circuit on the AerSimulator
#job = back1.run(circ_transpiled)
#result = job.result()

# get the final statevector
# get_statevector requires the circuit reference; passing circ_transpiled is robust
#try:
#    statevector = result.get_statevector(circ_transpiled)
#except Exception:
    # fallback: if only one circuit was executed, get_statevector() without args may work
#    statevector = result.get_statevector()

#qa.PrintStatevector(statevector, nq_phase, msystem)

# process the results: extract the solution and compare with a classical solution
# can also check QPE by removing Rc and QPE inverses in the main circuit, and uncommenting below
#qa.PrintStatevector(statevector,nq_phase,msystem)
#qa.CheckQPE(statevector, nq_phase, msystem)
#sol = qa.ExtractSolution(statevector, nq_phase, msystem)
#msystem.CompareClassical(sol)

#print()
print(f"circuit size: {circ_transpiled.size()}")
latex_code = circ_transpiled.draw(
    output="latex_source",
    fold=25   # try 20–40
)
with open("circuit.tex", "w") as f:
    f.write(latex_code)

sim_noise = AerSimulator(noise_model=noise_model)
 
# Transpile circuit for noisy basis gates
passmanager = generate_preset_pass_manager(
    optimization_level=2, backend=sim_noise
)
circ_tnoise = passmanager.run(circ_init)
 
# Run and get counts
result_bit_flip = sim_noise.run(circ_tnoise, shots=4096).result()
counts_bit_flip = result_bit_flip.get_counts(0)
 
sorted_result = dict(sorted(counts_bit_flip.items(), key=lambda x: x[1], reverse=True))

print(f"res: {sorted_result}")
