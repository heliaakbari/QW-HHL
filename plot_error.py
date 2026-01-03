from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.quantum_info import hellinger_distance, Statevector
from qiskit_aer import AerSimulator
from qiskit.result import marginal_counts
from qiskit import QuantumCircuit, qasm2, transpile
import math
import copy
import pandas as pd
from qiskit import *

job_id = "d5ai3ohsmlfc739lip50"

service = QiskitRuntimeService(
    channel='ibm_quantum_platform',
    instance='crn:v1:bluemix:public:quantum-computing:us-east:a/0d2ac5b9c3f04daea9791d4175b6a65a:b1f1595c-44d1-46de-a635-ef174f8fd088::'
)
job = service.job(job_id)
results = job.result()

files_dir=f"./qasms/{job_id}/"
errors=[]

pubs = job.inputs['pubs'] 
circuits = [pub[0] for pub in pubs]

for i, qc in enumerate(results):


    # 1. Get Experimental Probability
    exp_dist = results[i].data.meas.get_counts() 
    total_shots = sum(exp_dist.values())
    exp_probs = {k: v/total_shots for k, v in exp_dist.items()}

    qc_ideal = QuantumCircuit.from_qasm_file(f"{files_dir}step_{i}.qasm")
    ideal_probs = Statevector.from_instruction(qc_ideal).probabilities_dict()    
    # deep_copy = copy.deepcopy(exp_probs)
    # ideal_probs = {k: 0 for k, v in deep_copy.items()}  
    # ideal_probs['000000000'] = 0.25
    # ideal_probs['001000000'] = 0.25
    # ideal_probs['000100000'] = 0.25
    # ideal_probs['001100000'] = 0.25    

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
print(df)