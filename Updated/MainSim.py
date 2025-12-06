# references are made to arXiv:2112.02600 (accurate as of v3)
import sys
import time
import qiskit as qk
import MatrixProcedures as mp
import QAlgs as qa
import QWOps as qw
from qiskit_aer import AerSimulator
from qiskit.circuit.library import Initialize

tstart = time.time()
sim = AerSimulator(method="statevector")   # or AerSimulator() and default is "statevector"
print("Simulator:", sim)

outfile_path = "./output.txt"

# the choice of nq_phase affects the accuracy of QPE
nq_phase = 2
MM = 2

# initialize the matrix equation, and prepare it for the quantum procedure
print("Building system... ", end="")
sys.stdout.flush()
msystem = mp.MatrixSystem(M=MM, expand=False)
msystem.MoMInit()
msystem.PrepSystem()
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

print(circ.draw(output="text"))

print("Finished building circuit.")
print("Size of logical circuit: ", circ.size())
# transpile the circuit
print()
print("Transpiling... ", end="")
sys.stdout.flush()
circ_transpiled = qk.transpile(circ, sim, optimization_level=3)
print("Done.")
sys.stdout.flush()
print("Size of transpiled circuit: ", circ_transpiled.size())

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

print()
print("Miscellaneous items:")
print("%d %d %f" % (msystem.N, circ_transpiled.size(), time.time() - tstart))

# write summary to file
with open(outfile_path, "w") as outfile:
    outfile.write(str(msystem.N) + "\n")
    outfile.write(str(sum([len(x) for x in msystem.A_indices[:]])) + "\n")
    outfile.write(str(circ_transpiled.size()) + "\n")
    outfile.write(str(time.time() - tstart) + "\n")
