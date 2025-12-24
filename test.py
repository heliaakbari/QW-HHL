import numpy as np

# ---------------------------
# Basic quantum gates
# ---------------------------
def X_gate():
    return np.array([[0, 1],
                     [1, 0]], dtype=complex)

def P_gate(omega):
    return np.array([[1, 0],
                     [0, np.exp(1j * omega)]], dtype=complex)

def Ry_gate(theta):
    return np.array([[np.cos(theta), -np.sin(theta)],
                     [np.sin(theta),  np.cos(theta)]], dtype=complex)

# ---------------------------
# Algorithm 2 implementation
# ---------------------------
def compute_theta_omega(A, j, k, N, X_val):
    """
    Compute theta_jk and omega_jk for a given matrix A and indices j,k
    """
    A_jk = A[j, k]

    # theta_jk
    theta = np.arccos(np.sqrt(np.abs(A_jk) * N / X_val))

    # omega_jk
    omega = -np.angle(A_jk) / 2

    # special condition
    if np.angle(A_jk) == np.pi and j < k:
        omega = -omega

    return theta, omega

def XPXR_operation(theta, omega):
    """
    Compute X P(omega) X Ry(2theta)
    """
    X = X_gate()
    P = P_gate(omega)
    Ry = Ry_gate(2 * theta)

    return X @ P @ X @ Ry

# ---------------------------
# Full matrix processing
# ---------------------------
def process_matrix(A, N, X_val):
    """
    For each (j,k), return theta, omega, and matrices
    """
    results = {}
    rows, cols = A.shape

    for j in range(rows):
        for k in range(cols):
            theta, omega = compute_theta_omega(A, j, k, N, X_val)

            P = P_gate(omega)
            Ry = Ry_gate(2 * theta)
            XPXR = XPXR_operation(theta, omega)

            results[(j, k)] = {
                "theta": theta,
                "omega": omega,
                "P(omega)": P,
                "Ry(2theta)": Ry,
                "XPXR": XPXR
            }

    return results

def hermitian_from_eigendecomposition(eigenvalues, eigenvectors):
    """
    Construct a Hermitian matrix from eigenvalues and eigenvectors.

    Parameters
    ----------
    eigenvalues : array-like, shape (n,)
        Real eigenvalues.
    eigenvectors : array-like, shape (n, n)
        Columns are orthonormal eigenvectors.

    Returns
    -------
    H : ndarray, shape (n, n)
        Hermitian matrix.
    """
    eigenvalues = np.asarray(eigenvalues)
    V = np.asarray(eigenvectors)

    # Diagonal matrix of eigenvalues
    D = np.diag(eigenvalues)

    # Hermitian reconstruction: H = V D V†
    H = V @ D @ V.conj().T

    return H

def hermitian_imposed_constraints(eigenvalues, eigenvectors, d, X):
    """
    Construct a Hermitian matrix from eigenvalues/eigenvectors
    and impose diagonal and magnitude constraints by construction.

    Parameters
    ----------
    eigenvalues : (n,) array-like
        Real eigenvalues.
    eigenvectors : (n, n) array-like
        Orthonormal eigenvectors (columns).
    d : float
        Enforce A_ii >= -d
    X : float
        Enforce X >= n * max(|A_jk|)

    Returns
    -------
    A : (n, n) ndarray
        Hermitian matrix with imposed constraints.
    """

    eigenvalues = np.asarray(eigenvalues, dtype=float)
    V = np.asarray(eigenvectors, dtype=complex)

    n = len(eigenvalues)

    # 1. Base Hermitian matrix
    Λ = np.diag(eigenvalues)
    A = V @ Λ @ V.conj().T
    A = 0.5 * (A + A.conj().T)

    # 2. Impose diagonal lower bound by identity shift
    min_diag = np.min(np.real(np.diag(A)))
    if min_diag < -d:
        shift = (-d - min_diag)
        A = A - shift * np.eye(n)

    # 3. Impose magnitude bound by global scaling
    max_abs = np.max(np.abs(A))
    if max_abs > 0:
        scale = min(1.0, X / (n * max_abs))
        A = scale * A

    return A

A = np.array([[0, 0, 0.5, -0.5],
              [0, 0, -0.5,  0.5],
              [0.5, -0.5, 0, 0],
              [-0.5, 0.5, 0, 0]
              ], dtype=complex)

A = 2* np.array([[0, 0, 0.5, -0.5],
              [0, 0, -0.5,  0.5],
              [0.5, -0.5, 0, 0],
              [-0.5, 0.5, 0, 0]
              ], dtype=complex)

A1 = np.array([[1, 1],
              [1, 1],
              ], dtype=complex)

A= np.array([[-1, 0, 1, -1],
              [0, -1, -1,  1],
              [1, -1, -1, 0],
              [-1, 1, 0, -1]
              ], dtype=complex)

N = 4
X_val = 4
d= 1

eigenvalues = np.array([-d, X_val-d, -d, -X_val-d])

# Example eigenvectors (orthonormal columns)
V = np.array([
    [0.5,  0.5, 0.5, 0.5],
    [0.5,  -0.5, 0.5, -0.5],
    [0.5,  0.5, -0.5, -0.5], 
    [0.5,  -0.5, -0.5, 0.5],
], dtype=complex)

#A = hermitian_imposed_constraints(eigenvalues, V, -1, 2)

print("Hermitian matrix H:\n", A)

# Verify Hermitian property
print("Is Hermitian:", np.allclose(A, A.conj().T))



results = process_matrix(A, N, X_val)

for j in range(4):
    for k in range(4):
        print("theta:", results[(j, k)]["theta"])
        print("omega:", results[(j, k)]["omega"])
        print("P gate:\n", results[(j, k)]["P(omega)"])
        print("Ry gate:\n", results[(j, k)]["Ry(2theta)"])
        print("XPXR operation:\n", results[(j, k)]["XPXR"])