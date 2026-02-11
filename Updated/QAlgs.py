from qiskit import QuantumCircuit, QuantumRegister
import math
import numpy as np
from qiskit.circuit.library import PhaseGate, HGate, XGate, RYGate, SwapGate

EPSILON=1e-10

def PrintStatevector(sv, nq_phase, msystem):
    N_phase = int(2**nq_phase + EPSILON)
    N_work  = int(2**max(1, msystem.n - 1) + EPSILON) 
    N_work = 0
    N_main  = int(2**msystem.n + EPSILON)

    nq_work = max(1, msystem.n - 1) 
    nq_work = 0

    f_a = "{:01b}"
    f_w = "{:0%db}" % nq_work
    f_m = "{:0%db}" % msystem.n
    f_p = "{:0%db}" % nq_phase

    print(
        "|%s>|%s>|%s>|%s>|%s>|%s>" % (
            "rp".ljust(max(2, nq_phase)),
            "r1".ljust(max(2, msystem.n)),
            "r1a",
            "r2".ljust(max(2, msystem.n)),
            "r2a",
            "HHL"
        )
    )

    c_tot = 0
    for c_p in range(N_phase):
        s_p = f_p.format(c_p)
        for c_r1 in range(N_main):
            s_r1 = f_m.format(c_r1)
            for c_r1a in range(2):
                s_r1a = f_a.format(c_r1a)
                for c_r2 in range(N_main):
                    s_r2 = f_m.format(c_r2)
                    for c_r2a in range(2):
                        s_r2a = f_a.format(c_r2a)
                        for c_hhl in range(2):
                            s_hhl = f_a.format(c_hhl)
                            amp = sv[c_tot]
                            print(
                                "%.6f+%.6fi" %
                                (
                                    amp.real,
                                    amp.imag
                                )
                            )
                            c_tot += 1

def CheckQPE(sv, nq_phase, msystem):
    N_phase = int(2**nq_phase + EPSILON)
    N_work = int(2**max(1, msystem.n - 1) + EPSILON)
    f_phase = "{:0%db}" % nq_phase

    block_size = (
        msystem.N *
        N_work *
        2 *
        msystem.N *
        N_work *
        2 *
        2
    )

    probs = np.zeros(N_phase)
    for p in range(N_phase):
        start = p * block_size
        end   = start + block_size
        block = sv[start:end]
        probs[p] = np.sum(block.real**2 + block.imag**2)

    probs = probs / np.sum(probs)

    print(sv)
    print('-------------------------------------------------')
    print('| phase > register analysis:')
    print("X =", msystem.X, ",   d =", msystem.d)

    for p in range(N_phase):
        p_bits = f_phase.format(p)
        phi = p / float(N_phase)
        lam = msystem.bnorm * (
            math.sin(2.0 * math.pi * phi) * msystem.X - msystem.d
        )
        print(
            "|%s,  lambda=%10.6f >:   prob = %.6f ;   phi = %.6f"
            % (p_bits, lam.real, probs[p], phi)
        )

def ExtractSolution(sv: np.ndarray, nq_phase: int, msystem):
    N_phase=int(math.pow(2.0,nq_phase)+EPSILON)
    N_work=int(math.pow(2.0,max(1,msystem.n-1))+EPSILON)
    sol = np.zeros(msystem.N, dtype=complex)

    step = N_work * 2 * msystem.N * N_work * 2 * 2
    for j in range(msystem.N):
        idx = j * step
        if idx < len(sv):
            sol[j] = sv[idx]
        else:
            sol[j] = 0.0

    # calculate C
    if(msystem.d/msystem.X>1.0):
        C = abs(msystem.X-msystem.d)
    else:
        k0 = round(float(N_phase)/(2.0*math.pi) * math.asin(msystem.d/msystem.X))
        C1=abs(math.sin(2.0*math.pi*k0/float(N_phase))*msystem.X-msystem.d)
        C2=abs(math.sin(2.0*math.pi*(k0+1)/float(N_phase))*msystem.X-msystem.d)
        C3=abs(math.sin(2.0*math.pi*(k0-1)/float(N_phase))*msystem.X-msystem.d)
        if((k0-1)<0):
            C=min(C1,C2)
            if(C1<EPSILON):
                C=C2
        elif((k0+1)>=N_phase):
            C=min(C1,C3)
            if(C1<EPSILON):
                C=C3
        else:
            # *Note: only one can be zero
            if(C1<EPSILON):
                C=min(C2,C3)
            elif(C2<EPSILON):
                C=min(C1,C3)
            elif(C3<EPSILON):
                C=min(C1,C2)
            else:
                C=min(C1,C2,C3)
    C=C*(1.-EPSILON)

    print("C =", C)
    print("-------------------------------------------------")
    print("Solution:")
    print("b =", msystem.b)
    print("raw amplitudes =", sol)

    ret_val = np.zeros(msystem.M, dtype=complex)

    for j in range(msystem.M):
        if msystem.expand:
            ret_val[j] = sol[j + msystem.M] / C
        else:
            ret_val[j] = sol[j] / C

        print(f"{ret_val[j].real:.6f} + i({ret_val[j].imag:.6f}) -> |x|={abs(ret_val[j]):.6f}")

    return ret_val

# basic circuit for a quantum Fourier transform
def QFT(nq: int):
    reg = QuantumRegister(nq, name="q")
    circ = QuantumCircuit(reg, name="QFT")

    for i in range(nq):
        circ.append(HGate(), [reg[nq - 1 - i]])
        k = 1
        for j in range(i + 1, nq):
            angle = math.pi / (2 ** k)
            circ.cp(angle, reg[nq - 1 - j], reg[nq - 1 - i])
            k += 1

    for i in range(nq // 2):
        circ.append(SwapGate(), [reg[i], reg[nq - 1 - i]])

    return circ.to_gate(label=f"QFT_{nq}")

def QPE(U, nq_phase, nq_vec):
    reg_phase = QuantumRegister(nq_phase, "phase")
    reg_vec   = QuantumRegister(nq_vec,   "vec")
    circ = QuantumCircuit(reg_phase, reg_vec, name="QPE")
    Uc = U.control(1)
    for i in range(nq_phase):
        circ.h(reg_phase[nq_phase - 1 - i])

    for i in range(nq_phase):
        power = 2**i
        for _ in range(power):
            circ.append(Uc, [reg_phase[i], *reg_vec])

    circ.append(QFT(nq_phase).inverse(), reg_phase)
    return circ.to_gate(label=f"QPE_{nq_phase}")

# basic circuit for HHL rotation (Fig. 7 on p. 12)
def HHLRotation(nq_phase, msystem):
    reg_phase = QuantumRegister(nq_phase, "phase")
    reg_a = QuantumRegister(1, "anc")
    circ = QuantumCircuit(reg_phase, reg_a, name="HHL_Rotation")
    N_phase = 2 ** nq_phase
# calculate C
    if(msystem.d/msystem.X>1.0):
        C = abs(msystem.X-msystem.d)
    else:
        k0 = round(float(N_phase)/(2.0*math.pi) * math.asin(msystem.d/msystem.X))
        C1=abs(math.sin(2.0*math.pi*k0/float(N_phase))*msystem.X-msystem.d)
        C2=abs(math.sin(2.0*math.pi*(k0+1)/float(N_phase))*msystem.X-msystem.d)
        C3=abs(math.sin(2.0*math.pi*(k0-1)/float(N_phase))*msystem.X-msystem.d)
        if((k0-1)<0):
            C=min(C1,C2)
            if(C1<EPSILON):
                C=C2
        elif((k0+1)>=N_phase):
            C=min(C1,C3)
            if(C1<EPSILON):
                C=C3
        else:
            # *Note: only one can be zero
            if(C1<EPSILON):
                C=min(C2,C3)
            elif(C2<EPSILON):
                C=min(C1,C3)
            elif(C3<EPSILON):
                C=min(C1,C2)
            else:
                C=min(C1,C2,C3)
    C=C*(1.-EPSILON)
    print(C)
    fmt = "{:0" + str(nq_phase) + "b}"

    # Loop over all k basis states
    for k in range(N_phase):
        bitstring = fmt.format(k)

        phi = k / N_phase
        lam = math.sin(2 * math.pi * phi) * msystem.X - msystem.d

        if abs(lam) <= EPSILON:
            continue

        theta = 2 * math.acos(C / lam)
        mc_gate = RYGate(theta).control(nq_phase)

        # X-gate pre-conditioning for matching bitstring
        for i, b in enumerate(reversed(bitstring)):  
            # NOTE: reversed() makes bit 0 = reg_phase[0]
            if b == "0":
                circ.x(reg_phase[i])

        # Apply multi-controlled RY
        circ.append(mc_gate, [*reg_phase, reg_a[0]])

        # Undo X-gates
        for i, b in enumerate(reversed(bitstring)):
            if b == "0":
                circ.x(reg_phase[i])

    return circ.to_gate(label="HHL_Rotation")
