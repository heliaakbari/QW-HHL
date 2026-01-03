import sys
import math
import qiskit as qk
import MatrixProcedures as mp
from qiskit import *
from qiskit.circuit.library import HGate, XGate, RYGate, SwapGate, ZGate, SGate, CZGate
from qiskit_ibm_runtime.fake_provider import FakeGuadalupeV2
from qiskit.circuit.library import Initialize
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import (
    Batch,
    SamplerV2 as Sampler,
    EstimatorV2 as Estimator,
)

EPSILON=1e-10
shots=1024

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
######################################################################################################
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
######################################################################################################
#result
print(circ_init.draw(output="latex_source"))

print("Finished building circuit.")
print("Size of logical circuit: ", circ_init.size())



# transpile the circuit
service = QiskitRuntimeService()
back1 = service.backend("ibm_fez")
print()
print("Transpiling... ", end="")
pm = generate_preset_pass_manager(optimization_level=1, backend=back1)
isa_circuit = pm.run(circ_init)
print("Done.")
print("Size of transpiled circuit: ", isa_circuit.size())
job_id = 0
with Batch(backend=back1):
    sampler = Sampler()
    job = sampler.run([isa_circuit], shots=1024)
    job_id = job.job_id()
    print(f"job id: {job_id}")

#print(service.job(job_id).result())