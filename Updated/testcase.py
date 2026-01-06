import numpy as np

def generate_quantum_test_case(
    n,
    s,
    kappa_target,
    seed=None,
    zero_tol=1e-10
):
    """
    Generate a Hermitian, sparse, positive-definite matrix A
    for quantum linear solvers.

    Post-processing:
    - Small entries are zeroed
    - Eigenvalues are recomputed
    - Actual condition number is recalculated

    Returns a dictionary containing:
    - A
    - b
    - x_true
    - dimension
    - sparsity
    - kappa_target
    - kappa_actual
    - eigenvalues
    """

    if seed is not None:
        np.random.seed(seed)

    if s > n:
        raise ValueError("Nonzeros per row cannot exceed matrix dimension")

    # -------------------------
    # Step 1: sparse Hermitian
    # -------------------------
    A = np.zeros((n, n))

    for i in range(n):
        cols = np.random.choice(
            [j for j in range(n) if j != i],
            size=s - 1,
            replace=False
        )

        for j in cols:
            val = np.random.uniform(0.1, 1.0)
            A[i, j] = val
            A[j, i] = val  # Hermitian symmetry

    # ---------------------------------
    # Step 2: positive diagonal entries
    # ---------------------------------
    for i in range(n):
        A[i, i] = np.sum(np.abs(A[i])) + 1.0

    # ------------------------------------------------
    # Step 3: spectral rescaling to target κ
    # ------------------------------------------------
    eigvals, eigvecs = np.linalg.eigh(A)
    eigvals = np.clip(eigvals, 1e-8, None)

    eigvals_scaled = 1 + (eigvals - eigvals.min()) * (
        kappa_target - 1
    ) / (eigvals.max() - eigvals.min())

    A = eigvecs @ np.diag(eigvals_scaled) @ eigvecs.T

    # -----------------------------------
    # Step 4: zero-out tiny entries
    # -----------------------------------
    A[np.abs(A) < zero_tol] = 0.0

    # Enforce exact Hermiticity after cleanup
    A = 0.5 * (A + A.T)

    # -----------------------------------
    # Step 5: recompute spectrum & κ
    # -----------------------------------
    eigenvalues = np.linalg.eigvalsh(A)
    lambda_min = np.min(eigenvalues)
    lambda_max = np.max(eigenvalues)

    kappa_actual = lambda_max / lambda_min

    # -----------------------------------
    # Step 6: recompute sparsity
    # -----------------------------------
    nonzeros_per_row = np.count_nonzero(A, axis=1)
    sparsity_actual = int(nonzeros_per_row.max())

    # -----------------------------------
    # Step 6: generate solution and RHS
    # -----------------------------------
    x_true = np.random.randn(n)
    b = A @ x_true

    return {
        "A": A,
        "b": b,
        "x_true": x_true,
        "dimension": n,
        "sparsity_target": s,
        "sparsity_actual": sparsity_actual,
        "kappa_target": kappa_target,
        "kappa_actual": kappa_actual,
        "eigenvalues": eigenvalues
    }

test = generate_quantum_test_case(
    n=16,
    s=8,
    kappa_target=20,
    zero_tol=1e-9
)

print("A:", test["A"])
print("b:", test["b"])
print("x_true:", test["x_true"])
print("Dimension:", test["dimension"])
print("target Sparsity:", test["sparsity_target"])
print("actual Sparsity:", test["sparsity_actual"])
print("Target κ:", test["kappa_target"])
print("Actual κ:", test["kappa_actual"])
print("Eigenvalues:", test["eigenvalues"])

