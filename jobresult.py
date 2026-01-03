from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService(
    channel='ibm_quantum_platform',
    instance='crn:v1:bluemix:public:quantum-computing:us-east:a/0d2ac5b9c3f04daea9791d4175b6a65a:b1f1595c-44d1-46de-a635-ef174f8fd088::'
)
job = service.job('d5ai3ohsmlfc739lip50')
result = job.result()
 
# the data bin contains one BitArray
data = result[-1].data
print(f"Databin: {data}\n")
 
# to access the BitArray, use the key "meas", which is the default name of
# the classical register when this is added by the `measure_all` method
array = data.meas
counts = data.meas.get_counts()
sorted_result = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

print(f"Counts: {sorted_result}")
# To get counts for a particular pub result, use
#
# pub_result = job_result[<idx>].data.<classical register>.get_counts()
#
# where <idx> is the index of the pub and <classical register> is the name of the classical register.
# You can use circuit.cregs to find the name of the classical registers.