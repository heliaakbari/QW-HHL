import sys
import numpy as np
import math
from qiskit.quantum_info import Statevector
import qiskit as qk
from qiskit.quantum_info import Operator
import MatrixProcedures as mp
from qiskit import *
from qiskit.circuit.library import HGate, XGate, RYGate, SwapGate, ZGate, SGate, CZGate
from qiskit_ibm_runtime.fake_provider import FakeGuadalupeV2
from qiskit.circuit.library import Initialize
from qiskit import QuantumCircuit, qasm2 
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import (
    Batch,
    SamplerV2 as Sampler,
    EstimatorV2 as Estimator,
)

EPSILON=1e-10
shots=4096

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
C=1.9999999998
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
######################################################################################################

service = QiskitRuntimeService()
backend = service.backend("ibm_fez")

target_circuit = circ_init

qasm2.dump(target_circuit, f"./qasms/run1/whole.qasm")
    
threshold = 1000
num_instructions = len(target_circuit.data)
pm = generate_preset_pass_manager(optimization_level=2, backend=backend)

incremental_circuits = []
current_index = 0
step_counter = 0

print(f"Total instructions to process: {num_instructions}")

while current_index < num_instructions:
    # 1. Deduce the starting state classically
    # This represents the "perfect" state up to the current_index
    prefix_qc = qk.QuantumCircuit(reg_a_hhl, reg_r2a, reg_r2, reg_r1a, reg_r1, reg_phase)
    # Add all gates processed in previous segments
    prefix_data = target_circuit.data[:current_index]
    for inst, qargs, cargs in prefix_data:
        prefix_qc.append(inst, qargs, cargs)

    deduced_state = Statevector.from_instruction(prefix_qc)

    # 1. Ensure it's a complex128 for max precision
    data = np.array(deduced_state.data, dtype=np.complex128)

    # 2. Force hard normalization
    norm = np.linalg.norm(data)
    if norm == 0:
        raise ValueError("Statevector norm is zero!")
    data = data / norm

    # 3. Clip tiny values that cause precision noise in Isometry decomposition
    data[np.abs(data) < 1e-15] = 0

    # 4. Re-create the statevector
    deduced_state = Statevector(data)

    # 2. Always add exactly ONE gate per step
    actual_step_taken = 1
    # Create the circuit
    trial_qc = qk.QuantumCircuit(
        reg_a_hhl, reg_r2a, reg_r2, reg_r1a, reg_r1, reg_phase
    )
    trial_qc.prepare_state(deduced_state)
    trial_qc = trial_qc.decompose() # Decompose high-level state prep into gates
    # Add exactly one gate
    inst, qargs, cargs = target_circuit.data[current_index]
    trial_qc.append(inst, qargs, cargs)
    print(f"DEBUG: Processing gate {current_index}: {inst.name} on qubits {qargs}")
    trial_qc.measure_all()
    isa_qc = transpile(
            trial_qc, 
            backend=backend, 
            optimization_level=3  
        )
    incremental_circuits.append(isa_qc)

    print(
        f"Segment {step_counter}: "
        f"Processed gate {current_index}"
        f"transpiled size {isa_qc.size()}"
    )

    # Move forward by exactly one gate
    current_index += 1
    step_counter += 1


job_id = 0
with Batch(backend=backend):
    sampler = Sampler()
    job = sampler.run(incremental_circuits, shots=4096)
    job_id = job.job_id()
    print(f"job id: {job_id}")
