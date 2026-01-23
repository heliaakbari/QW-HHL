# references are made to arXiv:2112.02600 (accurate as of v3)
import sys
import time
import psutil
import os
import qiskit as qk
from qiskit.quantum_info import Operator
import MatrixProcedures as mp
import QAlgs as qa
import QWOps as qw
from qiskit_aer import AerSimulator
from qiskit.circuit.library import Initialize
import logging
import os
from datetime import datetime
import argparse

def print_resources():
    process = psutil.Process(os.getpid())
    
    # Memory usage in MB
    mem_info = process.memory_info()
    rss_mb = mem_info.rss / 1024 / 1024
    
    # CPU usage (can be >100% if multi-threaded)
    cpu_usage = process.cpu_percent(interval=1.0)
    
    print(f"--- Resource Monitor ---")
    print(f"Memory (RSS): {rss_mb:.2f} MB")
    print(f"CPU Usage: {cpu_usage}%")
    print(f"Threads: {process.num_threads()}")

class PrintToLogger:
    def __init__(self, logger):
        self.logger = logger

    def write(self, message):
        if message.strip():
            self.logger.info(message.strip())

    def flush(self):
        pass

def handleLogging():
    os.makedirs("logs", exist_ok=True)

    log_filename = datetime.now().strftime(f"logs/DEBUG_{sys.argv[1]}_{sys.argv[2]}_%Y-%m-%d_%H-%M-%S.log")

    logger = logging.getLogger("my_app")
    logger.setLevel(logging.INFO)

    # Prevent logs from other libraries
    logger.propagate = False

    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    sys.stdout = PrintToLogger(logger)
    sys.stderr = PrintToLogger(logger)

handleLogging()

# parser = argparse.ArgumentParser()
# parser.add_argument("--dimension", type=int, required=False)
# parser.add_argument("--phase", type=int, required=False)
# parser.add_argument("--kappa", type=float, required=False)
# parser.add_argument("--seed", type=int, required=False)
# parser.add_argument("--mode", required=False)


# args = parser.parse_args()

#print(f"mode: {args.mode}, dimension: {args.dimension}, phase: {args.phase}, kappa: {args.kappa}, seed: {args.seed}")

tstart = time.time()
#sim = AerSimulator(method="statevector", device="GPU", cuStateVec_enable=True)
sim = AerSimulator(
    method="statevector",
    device="CPU",
    cuStateVec_enable=True,
)
#sim = AerSimulator(method="statevector")   # or AerSimulator() and default is "statevector"
print("Simulator:", sim)
print(AerSimulator().available_devices())
outfile_path = "./output.txt"

# the choice of nq_phase affects the accuracy of QPE
# nq_phase = args.phase
# MM = args.dimension
nq_phase = int(sys.argv[3])
MM = int(sys.argv[1])

# initialize the matrix equation, and prepare it for the quantum procedure
print("Building system... ", end="")
sys.stdout.flush()
msystem = mp.MatrixSystem(M=MM, expand=False)

# if args.mode == "kappatest":
#     msystem.TestCaseInit_Kappa(D=MM, kappa_target=args.kappa, seed=args.seed)
#     msystem.PrepSystem()
# else:
msystem.FileInitMatlab(A_file="./benchmarks/matrix_"+sys.argv[1]+"_"+sys.argv[2]+".dat", b_file="./benchmarks/rvec_"+sys.argv[1]+"_"+sys.argv[2]+".dat")
msystem.PrepSystem()

print(f"msystem.d is {msystem.d} and msystem.X is {msystem.X}")
print("Done.")
msystem.PrintMatrix()

# construct the top-level operators
qw_ops = qw.Operators(msystem)
print("b =", msystem.b)

init = Initialize(msystem.b)
init.label = "Init"   # label the initialize gate (safer than .copy in some versions)

print()
print("Initializing...")
sys.stdout.flush()

T0 = qw_ops.T0()
T0.label = "T0"
print("T0 built")
sys.stdout.flush()

W = qw_ops.W()
W.label = "W"
print("W built")
sys.stdout.flush()

QPE = qa.QPE(W, nq_phase, max(4 * msystem.n, 6))
QPE.label = f"QPE_{nq_phase}"
print("QPE built")
sys.stdout.flush()

Rc = qa.HHLRotation(nq_phase, msystem)
Rc.label = "Rc"
print("Rc built")
sys.stdout.flush()

print("Finished initialization.")

# initialize the quantum system itself
reg_phase = qk.QuantumRegister(nq_phase, name="phase")
reg_r1 = qk.QuantumRegister(msystem.n, name="r1")
reg_r1w = qk.QuantumRegister(max(1, msystem.n - 1), name="r1w")
reg_r1a = qk.QuantumRegister(1, name="r1a")
reg_r2 = qk.QuantumRegister(msystem.n, name="r2")
reg_r2w = qk.QuantumRegister(max(1, msystem.n - 1), name="r2w")
reg_r2a = qk.QuantumRegister(1, name="r2a")
reg_a_hhl = qk.QuantumRegister(1, name="ah")
circ = qk.QuantumCircuit(
    reg_a_hhl,
    reg_r2a,
    reg_r2w,
    reg_r2,
    reg_r1a,
    reg_r1w,
    reg_r1,
    reg_phase,
    name="HHL_main",
)

print()
print("Building circuit...")
sys.stdout.flush()

# init register r1 with classical vector
circ.append(init, reg_r1[:])
circ.append(T0, reg_r1[:] + reg_r1w[:] + reg_r1a[:] + reg_r2[:] + reg_r2w[:] + reg_r2a[:])
print("T0 added")
sys.stdout.flush()

circ.append(QPE, reg_phase[:] + reg_r1[:] + reg_r1w[:] + reg_r1a[:] + reg_r2[:] + reg_r2w[:] + reg_r2a[:])
print("QPE added")
sys.stdout.flush()

circ.append(Rc, reg_phase[:] + reg_a_hhl[:])
print("Rc added")
sys.stdout.flush()

circ.append(QPE.inverse(), reg_phase[:] + reg_r1[:] + reg_r1w[:] + reg_r1a[:] + reg_r2[:] + reg_r2w[:] + reg_r2a[:])
print("QPE* added")
sys.stdout.flush()

circ.append(T0.inverse(), reg_r1[:] + reg_r1w[:] + reg_r1a[:] + reg_r2[:] + reg_r2w[:] + reg_r2a[:])
print("T0* added")
sys.stdout.flush()

#print(circ.draw(output="text"))

print("Finished building circuit.")

# transpile the circuit
print()
print("Transpiling... ", end="")
sys.stdout.flush()
circ_transpiled = qk.transpile(circ, sim, optimization_level=2)
print("Done.")
sys.stdout.flush()
print("Size of transpiled circuit: ", circ_transpiled.size())
print("Depth of transpiled circuit: ", circ_transpiled.depth())
print("Number of qubits in circuit: ", circ_transpiled.num_qubits)
circ_transpiled.save_statevector()
# run the circuit and extract results
print()
print("Running circuit... ", end="")
sys.stdout.flush()

# Run the transpiled circuit on the AerSimulator
job = sim.run(circ_transpiled)
result = job.result()

# get the final statevector
# get_statevector requires the circuit reference; passing circ_transpiled is robust
try:
    statevector = result.get_statevector(circ_transpiled)
except Exception:
    # fallback: if only one circuit was executed, get_statevector() without args may work
    statevector = result.get_statevector()

print("Done.")
#qa.PrintStatevector(statevector, nq_phase, msystem)
# process the results: extract the solution and compare with a classical solution
# can also check QPE by removing Rc and QPE inverses in the main circuit, and uncommenting below
#qa.PrintStatevector(statevector,nq_phase,msystem)
#qa.CheckQPE(statevector, nq_phase, msystem)
sol = qa.ExtractSolution(statevector, nq_phase, msystem)
msystem.CompareClassical(sol)

print_resources()

print("Miscellaneous items:")
print("%d %d %f" % (msystem.N, circ_transpiled.size(), time.time() - tstart))
