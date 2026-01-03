import sys
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

######################################################################################################
'''
step_size = 3
threshhold = 1000
num_instructions = len(target_circuit.data)
print(f"number of instructions: {num_instructions}")
incremental_circuits = []
pm = generate_preset_pass_manager(optimization_level=1, backend=backend)

# Iterate through the circuit in steps
for i in range(0, num_instructions, step_size):
    # 1. Create the Prefix (all gates up to the current step)
    prefix_qc = qk.QuantumCircuit(reg_a_hhl, reg_r2a, reg_r2, reg_r1a, reg_r1, reg_phase)
    prefix_qc.append(init,reg_r1)
    prefix_data = target_circuit.data[:i]
    for inst, qargs, cargs in prefix_data:
        prefix_qc.append(inst, qargs, cargs)
    
    deduced_state = Statevector.from_instruction(prefix_qc)

    # 3. Create the "New" Step Circuit
    step_qc = qk.QuantumCircuit(reg_a_hhl, reg_r2a, reg_r2, reg_r1a, reg_r1, reg_phase)
    step_qc.prepare_state(deduced_state)
    
    # 4. Add the next 'step_size' gates
    current_slice = target_circuit.data[i : i + step_size]
    for inst in current_slice:
        step_qc.append(inst)
    
    step_qc.measure_all()
    print(f"Size of logical circuit of step {i} = {step_qc.size()}")
    transpiled_step_qc = pm.run(step_qc)
    print(f"Size of transpiled circuit of step {i} = {transpiled_step_qc.size()}")
    incremental_circuits.append(step_qc)
'''
service = QiskitRuntimeService()
backend = service.backend("ibm_fez")

target_circuit = circ_init

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
    prefix_qc.append(init, reg_r1)
    
    # Add all gates processed in previous segments
    prefix_data = target_circuit.data[:current_index]
    for inst, qargs, cargs in prefix_data:
        prefix_qc.append(inst, qargs, cargs)
    
    deduced_state = Statevector.from_instruction(prefix_qc)

    # 2. Dynamically find how many gates we can add
    step_size = 1
    best_qc_for_this_step = None
    
    while current_index + step_size <= num_instructions:
        # Create a trial circuit
        trial_qc = qk.QuantumCircuit(reg_a_hhl, reg_r2a, reg_r2, reg_r1a, reg_r1, reg_phase)
        trial_qc.prepare_state(deduced_state)
        
        # Add a slice of gates
        trial_slice = target_circuit.data[current_index : current_index + step_size]
        for inst, qargs, cargs in trial_slice:
            trial_qc.append(inst, qargs, cargs)
        
        # Transpile to check the real hardware cost
        transpiled_trial = pm.run(trial_qc)
        gate_count = transpiled_trial.size()
        
        if gate_count <= threshold:
            # It fits! Save this as the best candidate and try adding one more gate
            best_qc_for_this_step = trial_qc
            step_size += 1
        else:
            # It's too big! Use the previous version that fit
            print(f"Step {step_counter}: Limit reached at {gate_count} gates. Slicing here.")
            break
    
    # If even 1 gate + state_prep is > threshold, we have to take it anyway or stop
    if best_qc_for_this_step is None:
        print(f"Warning: State preparation alone exceeds threshold at index {current_index}")
        # Fallback: just take the 1-gate version
        best_qc_for_this_step = trial_qc 
        actual_step_taken = 1
    else:
        actual_step_taken = step_size - 1

    # 3. Finalize this segment
    qc_decomposed = transpile(
    best_qc_for_this_step,
    basis_gates=["u", "cx"],
    optimization_level=0)
    qasm2.dump(qc_decomposed, f"./qasms/run1/step_{step_counter}.qasm")
    
    best_qc_for_this_step.measure_all()
    best_qc_for_this_step_trans = pm.run(best_qc_for_this_step)
    incremental_circuits.append(best_qc_for_this_step_trans)
    
    print(f"Segment {step_counter}: Processed gates {current_index} to {current_index + actual_step_taken}")
    
    # Move the pointer forward
    current_index += actual_step_taken
    step_counter += 1

print(f"Total jobs created: {len(incremental_circuits)}")

job_id = 0
with Batch(backend=backend):
    sampler = Sampler()
    job = sampler.run(incremental_circuits, shots=1024)
    job_id = job.job_id()
    print(f"job id: {job_id}")
