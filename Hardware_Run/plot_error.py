from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.quantum_info import hellinger_distance, Statevector
from qiskit_aer import AerSimulator
from qiskit.result import marginal_counts
from qiskit import QuantumCircuit, qasm2, transpile
import math
import copy
import pandas as pd
from qiskit import *

#job_id = "d5kdetsjt3vs73dsb1sg"  # final 4-unknown results
job_id = "d5lv66c8d8hc73cg1fo0"  # final 2-unknown results

service = QiskitRuntimeService(
    channel='ibm_quantum_platform',
    instance='open-instance'
)
job = service.job(job_id)
results = job.result()

files_dir=f"./qasms/Trial2_short/"
errors=[]

pubs = job.inputs['pubs'] 
circuits = [pub[0] for pub in pubs]

for i, qc in enumerate(results):


    # 1. Get Experimental Probability
    if i < 100 or True:
        exp_dist = results[i].data.meas.get_counts() 
        total_shots = sum(exp_dist.values())
        exp_probs = {k: v/total_shots for k, v in exp_dist.items()}
    
        qc_ideal = QuantumCircuit.from_qasm_file(f"{files_dir}step_{i}.qasm")
        ideal_probs = Statevector.from_instruction(qc_ideal).probabilities_dict()     
    
        print(f"gate size: {circuits[i].size()}")
        # 3. Calculate Error Metric
        metrics = {}
    
        metrics["hellinger"] = hellinger_distance(ideal_probs, exp_probs)
    
        all_states = set(exp_probs) | set(ideal_probs)
    
        metrics["tvd"] = 0.5 * sum(
            abs(exp_probs.get(x, 0) - ideal_probs.get(x, 0)) for x in all_states
        )
    
        metrics["fidelity"] = sum(
            math.sqrt(exp_probs.get(x, 0) * ideal_probs.get(x, 0)) for x in all_states
        )
    
        metrics["infidelity"] = 1 - metrics["fidelity"]
    
        errors.append({
        "step": i,
        **metrics
        })


df = pd.DataFrame(errors)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df)
