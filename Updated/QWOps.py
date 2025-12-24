from qiskit import QuantumCircuit, QuantumRegister
import math
import numpy as np
import MatrixProcedures
from qiskit.circuit.library import PhaseGate, HGate, XGate, RYGate
from qiskit.quantum_info import Operator
EPSILON = 1e-10

class Operators:

    def __init__(self, msystem):
        self.msystem = msystem

    # *Note: THIS NEEDS A CORRESPONDING UNDO OR THE BASE REGISTER BIT FLIPS WILL REMAIN
    def prepare_work(self, ctrl_bits):

        reg_base = QuantumRegister(self.msystem.n, "base")
        reg_work = QuantumRegister(max(1, self.msystem.n - 1), "work")
        circ = QuantumCircuit(reg_base, reg_work)

        ctrl_bits_flip = ctrl_bits[::-1]
        # switch desired 0's to 1's
        for p in range(self.msystem.n):
            if ctrl_bits_flip[p] == '0':
                circ.x(reg_base[p])

        # set work bits
        if self.msystem.n > 1:
            circ.ccx(reg_base[0], reg_base[1], reg_work[0])

            for p in range(1, self.msystem.n - 1):
                circ.ccx(reg_base[p + 1], reg_work[p - 1], reg_work[p])

        else:
            circ.cx(reg_base[0], reg_work[0])

        return circ.to_gate()

    # shorthand definition for negative identity operator
    def NI(self):
        qc = QuantumCircuit(1)
        qc.global_phase = np.pi
        return qc.to_gate(label="-I") 

    # shorthand definition for a factor of the imaginary unit    
    def iI(self):
        qc = QuantumCircuit(1)
        qc.global_phase = np.pi / 2
        return qc.to_gate(label="iI")
    
    # shorthand definition for the gate which modifies (only) the phase of the |0> state  
    def P1(self, phi):
        qc = QuantumCircuit(1)
        qc.x(0)
        qc.append(PhaseGate(phi), [0])
        qc.x(0)
        return qc.to_gate(label=f"P1({phi})")    
    
    # shorthand definition for the gate which negates (only) the component of the |0> state
    def Z1(self):
        qc = QuantumCircuit(1)
        qc.x(0)
        qc.z(0)
        qc.x(0)
        return qc.to_gate(label="Z1")    

    # prepares |phi_j> from the |0> state (Fig. 6 on p. 12)   
    def Bj(self, j):
        n = self.msystem.n
        reg_r2   = QuantumRegister(n, "r2")
        reg_r2w  = QuantumRegister(max(1, n - 1), "r2w")
        reg_r2a  = QuantumRegister(1, "a")
        circ = QuantumCircuit(reg_r2, reg_r2w, reg_r2a)
        format_str_k = '{:0%db}' % n
        # start in uniform superposition
        for k in range(n):
            circ.h(reg_r2[k])
        # NOT the ancilla
        circ.x(reg_r2a[0])
        # rotate ancilla to produce desired state
        for c in range(len(self.msystem.A_indices[j])):
            k_bits = format_str_k.format(self.msystem.A_indices[j][c])
            r = np.abs(self.msystem.A_elements[j][c])
            t = np.angle(self.msystem.A_elements[j][c])
            theta = np.arcsin(math.sqrt(r * self.msystem.N / self.msystem.X))
            omega = -0.5 * t
            if (abs(abs(t) - math.pi) < EPSILON) and (j < self.msystem.A_indices[j][c]):
                omega = -omega
            work_gate = self.prepare_work(k_bits)
            circ.append(work_gate, reg_r2[:] + reg_r2w[:])
            ry_gate = RYGate(-2.0 * theta).control(1, ctrl_state='1')
            ctrl_qubit = reg_r2w[max(0, n - 2)]
            circ.append(ry_gate, [ctrl_qubit] + [reg_r2a[0]])
            p1_gate = self.P1(omega).control(1, ctrl_state='1')
            circ.append(p1_gate, [ctrl_qubit] + [reg_r2a[0]])
            circ.append(work_gate.inverse(), reg_r2[:] + reg_r2w[:])
        print(circ.decompose().draw())
        return circ.to_gate(label=f"Bj({j})")
    
    # prepares |zeta_j> from the |0> state (no figure, quite trivial in our model. explained shortly after (57))
    def Bp(self):
        n = self.msystem.n
        reg_r2  = QuantumRegister(n, "r2")
        reg_r2a = QuantumRegister(1, "a")
        circ = QuantumCircuit(reg_r2, reg_r2a)
        # Flip the ancilla qubit to |1>
        circ.x(reg_r2a[0])
        return circ.to_gate(label="Bp")

    # conditional state preparation operator (Fig. 5 on p. 12)
    def T0(self):
        n = self.msystem.n
        reg_r1  = QuantumRegister(n, "r1")
        reg_r1w = QuantumRegister(max(1, n - 1), "r1w")
        reg_r1a = QuantumRegister(1, "r1a")
        reg_r2  = QuantumRegister(n, "r2")
        reg_r2w = QuantumRegister(max(1, n - 1), "r2w")
        reg_r2a = QuantumRegister(1, "r2a")
        circ = QuantumCircuit(reg_r1, reg_r1w, reg_r1a, reg_r2, reg_r2w, reg_r2a)
        format_str_j = "{:0%db}" % n
        # for each state of |r1>, prepare |r2>
        for j in range(self.msystem.N):
            j_bits = format_str_j.format(j)
            prep_gate = self.prepare_work(j_bits)
            circ.append(prep_gate, list(reg_r1) + list(reg_r1w))

            bj_gate = self.Bj(j).control(2, ctrl_state="01")
            ctrl_qubit_0 = reg_r1w[max(0, n - 2)]
            ctrl_qubit_1 = reg_r1a[0]
            target_qubits = list(reg_r2) + list(reg_r2w) + [reg_r2a[0]]
            circ.append(bj_gate, [ctrl_qubit_0, ctrl_qubit_1] + target_qubits)

            circ.append(prep_gate.inverse(), list(reg_r1) + list(reg_r1w))
        return circ.to_gate(label="T0")

    # the swap operation (includes ancilla bits) (no figure, defined in (24) on p. 5)
    def S(self):
        n = self.msystem.n
        reg_r1  = QuantumRegister(n, "r1")
        reg_r1a = QuantumRegister(1, "r1a")
        reg_r2  = QuantumRegister(n, "r2")
        reg_r2a = QuantumRegister(1, "r2a")
        circ = QuantumCircuit(reg_r1, reg_r1a, reg_r2, reg_r2a)
        for jk in range(n):
            circ.swap(reg_r1[jk], reg_r2[jk])
        circ.swap(reg_r1a[0], reg_r2a[0])
        return circ.to_gate(label="S")

    # reflection about the |0> state
    def R0(self):
        n = self.msystem.n
        reg_r2  = QuantumRegister(n, "r2")
        reg_r2w = QuantumRegister(max(1, n - 1), "r2w")
        reg_r2a = QuantumRegister(1, "a")
        circ = QuantumCircuit(reg_r2, reg_r2w, reg_r2a)
        #negate all states
        circ.append(self.NI(), [reg_r2a[0]])
        cstr = "0" * n
        # negate the all-|0>'s state
        prep_gate = self.prepare_work(cstr)
        circ.append(prep_gate, list(reg_r2) + list(reg_r2w))

        ctrl_qubit = reg_r2w[max(0, n - 2)]
        z1_ctrl = self.Z1().control(1, ctrl_state="1")
        circ.append(z1_ctrl, [ctrl_qubit, reg_r2a[0]])

        circ.append(prep_gate.inverse(), list(reg_r2) + list(reg_r2w))
        return circ.to_gate(label="R0")

    # reflection about |phi_j> (see (48) on p. 7)
    def RBj(self, j):
        n = self.msystem.n
        reg_r2  = QuantumRegister(n,   "r2")
        reg_r2w = QuantumRegister(max(1, n - 1), "r2w")
        reg_r2a = QuantumRegister(1,   "a")
        circ = QuantumCircuit(reg_r2, reg_r2w, reg_r2a)
        Bj = self.Bj(j)
        all_r2 = list(reg_r2) + list(reg_r2w) + [reg_r2a[0]]
        circ.append(Bj.inverse(), all_r2)
        circ.append(self.R0(), all_r2)
        circ.append(Bj, all_r2)
        return circ.to_gate(label=f"RBj({j})")

    # reflection about |zeta_j> (see (49) on p. 7)
    def RBp(self):
        n = self.msystem.n
        reg_r2  = QuantumRegister(n,   "r2")
        reg_r2w = QuantumRegister(max(1, n - 1), "r2w")
        reg_r2a = QuantumRegister(1,   "a")
        circ = QuantumCircuit(reg_r2, reg_r2w, reg_r2a)
        Bp = self.Bp()
        r2_and_a = list(reg_r2) + [reg_r2a[0]]
        full_r2 = list(reg_r2) + list(reg_r2w) + [reg_r2a[0]]
        circ.append(Bp.inverse(), r2_and_a)
        circ.append(self.R0(), full_r2)
        circ.append(Bp, r2_and_a)
        return circ.to_gate(label="RBp")
    
    # the walk operator (Fig. 9 on p. 14)
    def W(self):
        n = self.msystem.n
        reg_r1  = QuantumRegister(n, "r1")
        reg_r1w = QuantumRegister(max(1, n - 1), "r1w")
        reg_r1a = QuantumRegister(1, "r1a")
        reg_r2  = QuantumRegister(n, "r2")
        reg_r2w = QuantumRegister(max(1, n - 1), "r2w")
        reg_r2a = QuantumRegister(1, "r2a")
        circ = QuantumCircuit(reg_r1, reg_r1w, reg_r1a, reg_r2, reg_r2w, reg_r2a)
        format_str_j = "{:0%db}" % n
        for j in range(self.msystem.N):
            j_bits = format_str_j.format(j)

            prep_gate = self.prepare_work(j_bits)
            circ.append(prep_gate, list(reg_r1) + list(reg_r1w))

            rbj_gate = self.RBj(j).control(2, ctrl_state="01")
            ctrl_qubit_0 = reg_r1w[max(0, n - 2)]
            ctrl_qubit_1 = reg_r1a[0]
            target_qubits = list(reg_r2) + list(reg_r2w) + [reg_r2a[0]]
            circ.append(rbj_gate, [ctrl_qubit_0, ctrl_qubit_1] + target_qubits)

            circ.append(prep_gate.inverse(), list(reg_r1) + list(reg_r1w))

        rbp_gate = self.RBp().control(1, ctrl_state="1")
        circ.append(rbp_gate, [reg_r1a[0]] + list(reg_r2) + list(reg_r2w) + [reg_r2a[0]])

        circ.append(self.S(), list(reg_r1) + [reg_r1a[0]] + list(reg_r2) + [reg_r2a[0]])
        circ.append(self.iI(), [reg_r1[n - 1]])
        return circ.to_gate(label="W")    