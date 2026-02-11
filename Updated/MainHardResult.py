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
#[reg_phase bits][reg_r1 bits][reg_r1a bits][reg_r2 bits][reg_r2a bits][reg_a_hhl bits]
print(f"Counts: {counts}")

filtered = {
    k: v for k, v in counts.items()
    if not k.endswith("0")
}

sorted_items = sorted(filtered.items(), key=lambda x: (x[0][:2], x[0]))

labels = [k for k, _ in sorted_items]
values = [v for _, v in sorted_items]

color_map = {
    "00": "tab:blue",
    "01": "tab:orange",
    "10": "tab:green",
    "11": "tab:red"
}

colors = [color_map[k[:2]] for k in labels]

import matplotlib.pyplot as plt

plt.figure(figsize=(10,4))
plt.bar(labels, values, color=colors)
plt.xticks(rotation=90)
plt.xlabel("7-bit Binary Keys (sorted by first two bits)")
plt.ylabel("Value")
plt.title("Values Sorted by First Two Bits (Color-Coded)")
plt.tight_layout()
plt.show()
