import numpy as np

def verify_optimized_matrix(d):
    print(f"--- Verifying Optimized Matrix for d = {d} ---\n")

    # 1. Construct the K2,2 based Matrix A
    # Zeros on diagonal blocks, Ones on off-diagonal blocks
    A = np.array([
        [-d,  0,  1,  1],
        [ 0, -d,  1,  1],
        [ 1,  1, -d,  0],
        [ 1,  1,  0, -d]
    ])
    
    print("Matrix A:")
    print(A)
    print()

    # 2. Check "More 1s"
    # Count non-diagonal non-zeros
    A_plus_dI = A + d * np.eye(4)
    print(A_plus_dI)
    num_ones = np.count_nonzero(A_plus_dI)
    print(f"Number of 1s in off-diagonal positions: {num_ones}")

    # 3. Calculate Eigenvalues
    evals = np.linalg.eigvals(A)
    evals.sort()
    
    print(f"Calculated Eigenvalues: {evals}")
    
    # Target: -d-2, -d, -d, -d+2 (Since X=2)
    target_evals = np.array([-d-2, -d, -d, -d+2])
    target_evals.sort()
    
    if np.allclose(evals, target_evals):
        print(f">> Eigenvalues MATCH the pattern with X = 2.")
    else:
        print(">> Eigenvalues do NOT match.")
    print()

    # 4. Verify X Constraint
    X = 2
    max_abs_cell = np.max(np.abs(A_plus_dI))
    
    print(f"X: {X}")
    print(f"Max absolute cell of (A + dI): {max_abs_cell}")
    
    if X >= max_abs_cell:
        print(">> Constraint (X >= Max Abs Cell) is SATISFIED.")

verify_optimized_matrix(d=1)