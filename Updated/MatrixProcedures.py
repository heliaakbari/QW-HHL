from __future__ import annotations
import math
import random
import bisect
from typing import List
import numpy as np

EPSILON = 1e-10
i = 1j


class MatrixSystem:

    def __init__(self, M: int = 1, expand: bool = True):
        self.expand = expand 
        self.M = M 
        self.n = 0                 
        self.N = 0
        self.bnorm = 0.0
        self.d = 0.0
        self.ap = 0.0
        self.X = 0.0
        self.C = 0.0

        # sparse matrix storage
        self.A0_indices: List[List[int]] = []
        self.A0_elements: List[List[complex]] = []
        self.b0: List[complex] = []

        # expanded (block-encoding) versions created later
        self.A_indices: List[List[int]] = []
        self.A_elements: List[List[complex]] = []
        self.b: List[complex] = []

    #Load matrix from file
    def FileInit(self, A_file: str = "./Updated/MS.txt", b_file: str = "./Updated/b0.txt"):
        """Load A₀ and b₀ from text files."""
        self.A0_indices.clear()
        self.A0_elements.clear()
        self.b0.clear()

        with open(A_file, "r") as f:
            lines = f.readlines()
        current_row = -1
        for line in lines:
            j_str, k_str, v_str = line.split(",")
            j = int(j_str) - 1
            k = int(k_str) - 1
            value = complex(v_str)
            while current_row < j:
                current_row += 1
                self.A0_indices.append([])
                self.A0_elements.append([])
            self.A0_indices[j].append(k)
            self.A0_elements[j].append(value)
        with open(b_file, "r") as f:
            for line in f:
                self.b0.append(complex(line.strip()))

    # Method-of-Moments matrix
    def MoMInit(self):
        """parallel-strip Method of Moments test system."""
        self.A0_indices.clear()
        self.A0_elements.clear()
        self.b0.clear()

        l = 2.0 / float(self.M)
        positions = []

        # build source vector b₀ and geometry
        for j in range(self.M):
            if j < self.M // 2:
                self.b0.append(1.0)
                positions.append([-0.5, l * j - 0.5])
            else:
                self.b0.append(-1.0)
                positions.append([0.5, l * (j - self.M // 2) - 0.5])

        for j in range(self.M):
            row_idx = []
            row_val = []
            xj, yj = positions[j]

            for k in range(self.M):
                row_idx.append(k)
                xk, yk = positions[k]

                if j == k:
                    value = -l * (math.log(l) - 1.5)
                else:
                    r = math.sqrt((xj - xk) ** 2 + (yj - yk) ** 2)
                    value = -l * math.log(r)

                row_val.append(value)

            self.A0_indices.append(row_idx)
            self.A0_elements.append(row_val)

    def FullyQuantumInit(self):
        
        self.A0_indices = [
            [0, 1],   # Row 0 → columns containing values
            [0, 1]    # Row 1
        ]

        self.A0_elements = [
            [-2.0, 1.0],   # Row 0 entries
            [1.0, -2.0]    # Row 1 entries
        ]

        self.b0 = [1.0, 0.0]
        self.bnorm = 1

        self.A_indices = [
            [0, 1],   # Row 0
            [0, 1]    # Row 1
        ]

        self.A_elements = [
            [1.0, 1.0],   # Row 0 entries
            [1.0, 1.0]    # Row 1 entries
        ]

        self.b = [1.0, 0.0]

        #prepSystem
        self.n=1
        self.N=2
        self.ap=1
        self.d=3.0
        self.X=2.0+EPSILON 
        self.C = 0

    # Random sparse Hermitian
    def RandInit(self, D: int = 1):
        """
        Create a random sparse Hermitian matrix with approx D non-zeros per row.
        Guarantees diagonal entries exist so A₀ is non-singular.
        """
        self.A0_indices = [[j] for j in range(self.M)]   # always diagonal
        self.A0_elements = [[] for _ in range(self.M)]
        self.b0 = []

        # random sparsity pattern (Erdős–Rényi-like)
        for j in range(self.M):
            for _ in range(D - 1):
                k = random.randint(0, self.M - 1)
                if k not in self.A0_indices[j]:
                    # ensure symmetry of sparsity structure
                    bisect.insort(self.A0_indices[j], k)
                    bisect.insort(self.A0_indices[k], j)

        # assign Hermitian values
        for j in range(self.M):
            for k in self.A0_indices[j]:
                if k == j:
                    # real diagonal
                    x = 2.0 * (random.random() - 0.5)
                    self.A0_elements[j].append(complex(x, 0.0))
                elif k > j:
                    # random complex pair
                    x = 2.0 * (random.random() - 0.5)
                    y = 2.0 * (random.random() - 0.5)
                    self.A0_elements[j].append(complex(x, y))
                    self.A0_elements[k].append(complex(x, -y))

        # random RHS vector b₀
        for _ in range(self.M):
            x = 2.0 * (random.random() - 0.5)
            y = 2.0 * (random.random() - 0.5)
            self.b0.append(complex(x, y))

    def RandInitSeed(self, D: int = 1, seed=None):
        if seed is not None:
            random.seed(seed)

        self.A0_indices = [[j] for j in range(self.M)]
        self.A0_elements = [[] for _ in range(self.M)]
        self.b0 = []
        
        for j in range(self.M):
            for _ in range(D - 1):
                k = random.randint(0, self.M - 1)
                if k not in self.A0_indices[j]:
                    bisect.insort(self.A0_indices[j], k)
                    if j != k and k not in self.A0_indices[k]:
                        bisect.insort(self.A0_indices[k], j)

        generated_values = {}

        for j in range(self.M):
            for k in self.A0_indices[j]:
                if j == k:
                    x = 2.0 * (random.random() - 0.5)
                    value = complex(x, 0.0)
                    generated_values[(j, k)] = value
                    self.A0_elements[j].append(value)
                elif j < k:
                    x = 2.0 * (random.random() - 0.5)
                    y = 2.0 * (random.random() - 0.5)
                    value = complex(x, y)
                    generated_values[(j, k)] = value
                    self.A0_elements[j].append(value)
                else: 
                    conj_value = generated_values[(k, j)].conjugate()
                    self.A0_elements[j].append(conj_value)
                    
        for _ in range(self.M):
            x = 2.0 * (random.random() - 0.5)
            y = 2.0 * (random.random() - 0.5)
            self.b0.append(complex(x, y))

    def PrepSystem(self):
        """
        Prepare expanded or non-expanded block-encoded system (A, b).
        Normalizes the system, applies diagonal shift when needed,
        and calculates bounds required by the quantum algorithm.
        """
        # determine the appropriate size of the system for quantum operation
        if self.expand:
            self.n = math.ceil(math.log(self.M, 2) - EPSILON) + 1
            self.N = 2 ** self.n
        else:
            self.n = math.ceil(math.log(self.M, 2) - EPSILON)
            self.N = self.M

        self.A_indices = []
        self.A_elements = []
        self.b = []

        # set the elements of A and b
        if self.expand:
            self.A_indices = [[] for _ in range(self.N)]
            self.A_elements = [[] for _ in range(self.N)]

            self.b = list(self.b0[:self.M]) + [0.0] * (self.N - self.M)

            # Fill expanded Hermitian block matrix
            # Top-left block: 0
            # Top-right block:  A₀
            # Bottom-left block: A₀†
            # Bottom-right block: I  (for j >= 2M)
            for j in range(self.M):
                for c, k in enumerate(self.A0_indices[j]):
                    val = self.A0_elements[j][c]

                    # A₀ goes at (j, M+k)
                    self.A_indices[j].append(self.M + k)
                    self.A_elements[j].append(val)

                    # A₀† goes at (M+k, j)
                    self.A_indices[self.M + k].append(j)
                    self.A_elements[self.M + k].append(np.conjugate(val))

            # identity padding: rows 2M ... N-1
            for j in range(2 * self.M, self.N):
                self.A_indices[j].append(j)
                self.A_elements[j].append(1.0)

        else:
            # Non-expanded system: A = A₀, b = b₀
            for j in range(self.M):
                self.b.append(self.b0[j])
                self.A_indices.append(list(self.A0_indices[j]))
                self.A_elements.append(list(self.A0_elements[j]))

        # Normalize b and A by ‖b‖
        self.bnorm = math.sqrt(sum(abs(x) * abs(x) for x in self.b))
        for j in range(self.N):
            self.b[j] /= self.bnorm
            self.A_elements[j] = [elem / self.bnorm for elem in self.A_elements[j]]

        # Apply diagonal offset (only when NOT expanded)
        if self.expand:
            self.d = 0.0
        else:
            # find max diagonal magnitude
            self.d = 0.0
            for j in range(self.N):
                for idx, col in enumerate(self.A_indices[j]):
                    if col == j:  # diagonal found
                        self.d = max(self.d, abs(self.A_elements[j][idx]))
                    elif col > j:
                        break
            self.d = self.d+1
            # apply shift A ← A + dI
            for j in range(self.N):
                for idx, col in enumerate(self.A_indices[j]):
                    if col == j:
                        self.A_elements[j][idx] += self.d
                    elif col > j:
                        break

        # Compute upper bound X = N * max|Aᵢⱼ|
        self.ap = max(
            abs(elem)
            for row in self.A_elements
            for elem in row
        ) if self.A_elements else 0.0
        self.X = abs(self.N * self.ap + EPSILON)

    def CompareClassical(self, sol):
        """
        Compare the quantum solution `sol` to the classical solution A^{-1} b.
        """
        # Reconstruct dense A0 (M × M)
        A0 = np.zeros((self.M, self.M), dtype=complex)
        for j in range(self.M):
            for idx, col in enumerate(self.A0_indices[j]):
                A0[j, col] = self.A0_elements[j][idx]

        # Classical solution
        sol_class = np.linalg.solve(A0, self.b0)
        print(f"classical solution: {sol_class}")
        # Global phase alignment
        phase_rel = np.angle(sol_class[0]) - np.angle(sol[0])
        sol_aligned = sol * np.exp(1j * phase_rel)

        print("----------------------------")
        print("Solution Comparison:\n")
        print(f"{'Quantum':>24} | {'Classical':>24}")
        print("-" * 50)

        for j in range(self.M):
            q = sol_aligned[j]
            c = sol_class[j]
            print(f"{q.real:10.6f} + i({q.imag:10.6f}) | "
                f"{c.real:10.6f} + i({c.imag:10.6f})")

        print("\nRelative Errors:")
        rel_errors = np.abs(1 - sol_aligned / sol_class)
        for e in rel_errors:
            print(e)

        print("\nAverage Relative Error:", np.mean(rel_errors))


    def PrintMatrix(self):
        """
        Print the original matrix A0 (M × M) and expanded matrix A (N × N)
        using the sparse index representation.
        """

        # Print A0
        print("A0 (original matrix):\n")
        for j in range(self.M):
            row = []
            ptr = 0
            for k in range(self.M):
                if ptr < len(self.A0_indices[j]) and self.A0_indices[j][ptr] == k:
                    val = self.A0_elements[j][ptr]
                    ptr += 1
                else:
                    val = 0.0 + 0.0j
                row.append(f"{val.real:6.2f}+({val.imag:6.2f}) ")
            print("".join(row))
        print("\n")

        # Print A (expanded matrix)
        print("A (expanded/normalized system matrix):\n")
        for j in range(self.N):
            row = []
            ptr = 0
            for k in range(self.N):
                if ptr < len(self.A_indices[j]) and self.A_indices[j][ptr] == k:
                    val = self.A_elements[j][ptr]
                    ptr += 1
                else:
                    val = 0.0 + 0.0j
                row.append(f"{val.real:6.2f}+({val.imag:6.2f}) ")
            print("".join(row))
        print()
