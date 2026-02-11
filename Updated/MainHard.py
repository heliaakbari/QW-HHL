import sys
import math
import qiskit as qk
import MatrixProcedures as mp
import QAlgs as qa
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
#circ_init=qk.QuantumCircuit(reg_phase, reg_r1, reg_r1a, reg_r2, reg_r2a, reg_a_hhl)

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
# circ_init.append(HGate(),[reg_phase[1]])
# circ_init.append(CZGate().power(0.5),reg_phase)
# circ_init.append(HGate(),[reg_phase[0]])
# circ_init.append(SwapGate(),reg_phase)
# circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
# circ_init.append(SGate().inverse().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
# circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
# circ_init.append(SGate().inverse().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
# circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[1]]+reg_r1a[:]+reg_r2a[:])
# circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[1]]+reg_r1[:]+reg_r2[:])
# circ_init.append(XGate().control(2,None,'11'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2a[0]])
# circ_init.append(HGate().control(2,None,'01'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2[0]])
# circ_init.append(XGate().control(2,None,'01'),[reg_phase[1]]+reg_r2[:]+reg_r2a[:])
# circ_init.append(ZGate().control(2,None,'01'),[reg_phase[1]]+reg_r2[:]+reg_r2a[:])
# circ_init.append(XGate().control(2,None,'01'),[reg_phase[1]]+reg_r2[:]+reg_r2a[:])
# circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
# circ_init.append(ZGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
# circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
# circ_init.append(ZGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
# circ_init.append(XGate().control(2,None,'11'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2a[0]])
# circ_init.append(HGate().control(2,None,'01'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2[0]])
# circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
# circ_init.append(SGate().inverse().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
# circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
# circ_init.append(SGate().inverse().control(1,None,'1'),[reg_phase[1]]+[reg_r1[0]])
# circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[1]]+reg_r1a[:]+reg_r2a[:])
# circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[1]]+reg_r1[:]+reg_r2[:])
# circ_init.append(XGate().control(2,None,'11'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2a[0]])
# circ_init.append(HGate().control(2,None,'01'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2[0]])
# circ_init.append(XGate().control(2,None,'01'),[reg_phase[1]]+reg_r2[:]+reg_r2a[:])
# circ_init.append(ZGate().control(2,None,'01'),[reg_phase[1]]+reg_r2[:]+reg_r2a[:])
# circ_init.append(XGate().control(2,None,'01'),[reg_phase[1]]+reg_r2[:]+reg_r2a[:])
# circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
# circ_init.append(ZGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
# circ_init.append(XGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
# circ_init.append(ZGate().control(1,None,'1'),[reg_phase[1]]+[reg_r2[0]])
# circ_init.append(XGate().control(2,None,'11'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2a[0]])
# circ_init.append(HGate().control(2,None,'01'),[reg_phase[1]]+[reg_r1a[0]]+[reg_r2[0]])
# circ_init.append(XGate().control(1,None,'1'),[reg_phase[0]]+[reg_r1[0]])
# circ_init.append(SGate().inverse().control(1,None,'1'),[reg_phase[0]]+[reg_r1[0]])
# circ_init.append(XGate().control(1,None,'1'),[reg_phase[0]]+[reg_r1[0]])
# circ_init.append(SGate().inverse().control(1,None,'1'),[reg_phase[0]]+[reg_r1[0]])
# circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[0]]+reg_r1a[:]+reg_r2a[:])
# circ_init.append(SwapGate().control(1,None,'1'), [reg_phase[0]]+reg_r1[:]+reg_r2[:])
# circ_init.append(XGate().control(2,None,'11'),[reg_phase[0]]+[reg_r1a[0]]+[reg_r2a[0]])
# circ_init.append(HGate().control(2,None,'01'),[reg_phase[0]]+[reg_r1a[0]]+[reg_r2[0]])
# circ_init.append(XGate().control(2,None,'01'),[reg_phase[0]]+reg_r2[:]+reg_r2a[:])
# circ_init.append(ZGate().control(2,None,'01'),[reg_phase[0]]+reg_r2[:]+reg_r2a[:])
# circ_init.append(XGate().control(2,None,'01'),[reg_phase[0]]+reg_r2[:]+reg_r2a[:])
# circ_init.append(XGate().control(1,None,'1'),[reg_phase[0]]+[reg_r2[0]])
# circ_init.append(ZGate().control(1,None,'1'),[reg_phase[0]]+[reg_r2[0]])
# circ_init.append(XGate().control(1,None,'1'),[reg_phase[0]]+[reg_r2[0]])
# circ_init.append(ZGate().control(1,None,'1'),[reg_phase[0]]+[reg_r2[0]])
# circ_init.append(XGate().control(2,None,'11'),[reg_phase[0]]+[reg_r1a[0]]+[reg_r2a[0]])
# circ_init.append(HGate().control(2,None,'01'),[reg_phase[0]]+[reg_r1a[0]]+[reg_r2[0]])
# circ_init.append(HGate(),[reg_phase[1]])
# circ_init.append(HGate(),[reg_phase[0]])
# circ_init.barrier()
# # inverse T
# circ_init.append(HGate(),reg_r2)

######################################################################################################
#result

print("Finished building circuit.")
print("Size of logical circuit: ", circ_init.size())

# transpile the circuit for simulation
sim = AerSimulator(
    method="statevector",
    device="CPU",
    cuStateVec_enable=True,
)

circ_transpiled_sim = qk.transpile(circ_init, sim, optimization_level=2)
print("Done.")
sys.stdout.flush()
print("Size of transpiled circuit: ", circ_transpiled_sim.size())
print("Depth of transpiled circuit: ", circ_transpiled_sim.depth())
print("Number of qubits in circuit: ", circ_transpiled_sim.num_qubits)
circ_transpiled_sim.save_statevector()
# run the circuit and extract results
print()
print("Running circuit... ", end="")
sys.stdout.flush()

# Run the transpiled circuit on the AerSimulator
job = sim.run(circ_transpiled_sim)
result = job.result()

# get the final statevector
# get_statevector requires the circuit reference; passing circ_transpiled is robust
try:
    statevector = result.get_statevector(circ_transpiled_sim)
except Exception:
    # fallback: if only one circuit was executed, get_statevector() without args may work
    statevector = result.get_statevector()

print("Done.")
qa.PrintStatevector(statevector, nq_phase, msystem)
# process the results: extract the solution and compare with a classical solution
# can also check QPE by removing Rc and QPE inverses in the main circuit, and uncommenting below
#qa.PrintStatevector(statevector,nq_phase,msystem)
#qa.CheckQPE(statevector, nq_phase, msystem)
sol = qa.ExtractSolution(statevector, nq_phase, msystem)
msystem.CompareClassical(sol)
print("probability dict")
probs = statevector.probabilities_dict(qargs=None, decimals=None)
print(probs)
print(len([key for key in statevector.probabilities_dict(qargs=None, decimals=None)]))
# transpile the circuit for submission
"""
circ_init.measure_all()
service = QiskitRuntimeService()
back1 = service.backend("ibm_fez")
print()
print("Transpiling... ", end="")
pm = generate_preset_pass_manager(optimization_level=3, backend=back1)
isa_circuit = pm.run(circ_init)
print("Done.")
print("Size of transpiled circuit: ", isa_circuit.size())
job_id = 0
with Batch(backend=back1):
    sampler = Sampler()
    job = sampler.run([isa_circuit], shots=8192)
    job_id = job.job_id()
    print(f"job id: {job_id}")
"""
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.result import marginal_distribution

service = QiskitRuntimeService(
    channel='ibm_quantum_platform',
    instance='crn:v1:bluemix:public:quantum-computing:us-east:a/0d2ac5b9c3f04daea9791d4175b6a65a:b1f1595c-44d1-46de-a635-ef174f8fd088::'
)
job = service.job('d63ensbtraac73bh6dpg')
result = job.result()
 
# the data bin contains one BitArray
data = result[0].data
print(f"Databin: {data}\n")
 
# to access the BitArray, use the key "meas", which is the default name of
# the classical register when this is added by the `measure_all` method
array = data.meas
counts = data.meas.get_counts()


import matplotlib.pyplot as plt
import numpy as np

# 1. Define your dictionaries
# 1. Define your dictionaries
dict1 = probs 
new_dict = {}

for k, v in dict1.items():
    # swap first two digits
    new_key = k[1] + k[0] + k[2:]
    new_dict[new_key] = v
dict1 = new_dict
dict2 = counts



# 2. Create a sorted union of all keys from both dictionaries
all_keys = sorted([
    key for key in (set(dict1.keys()) | set(dict2.keys())) 
    if not str(key).endswith('1')
])
# 3. Extract values, defaulting to 0 if the key is missing
values1 = [dict1.get(key, 0) for key in all_keys]
values2 = [dict2.get(key, 0) for key in all_keys]

# Normalize both datasets to their maximum values
values1_norm = values1 / np.max(values1) if np.max(values1) != 0 else values1
values2_norm = values2 / np.max(values2) if np.max(values2) != 0 else values2

# Create a color map based on key prefix
# Create a color map based on key prefix
color_map = {'00': 'red', '01': 'green', '10': 'orange', '11': 'purple'}
bar_colors = [color_map.get(key[:2], 'grey') for key in all_keys]  # default grey if prefix unknown

fig, ax1 = plt.subplots(figsize=(15,8))

# Bar chart for the Simulated Statevector (values2) on the right y-axis
ax1.bar(all_keys, values2, color=bar_colors, alpha=0.6, label='IBM Runtime (counts out of 8192)')
ax1.set_ylabel('Counts in runtime')
ax1.tick_params(axis='y', labelcolor='blue')

# Create a second y-axis for values1
ax2 = ax1.twinx()
ax2.plot(all_keys, values1, color='black', marker='o', markersize=4, 
         linestyle='-', linewidth=2, label='Statevector (Simulation Probability)')
ax2.set_ylabel('Probability in simulation')
ax2.set_ylim(0, np.max(values1))
ax2.tick_params(axis='y', labelcolor='black')

# Combine legends
lines_labels = [ax.get_legend_handles_labels() for ax in [ax1, ax2]]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
ax1.legend(lines, labels, loc='upper right')
plt.subplots_adjust(bottom=0.5)

plt.xticks(rotation=45, fontsize=5)

plt.title("Comparison: Statevector vs. Hardware Results")
plt.tight_layout()
fig.autofmt_xdate(rotation=45)
plt.show()