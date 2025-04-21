import numpy as np
from scipy.sparse import coo_matrix


def read_file_to_sparse_matrix(file_path):
    """
    Reads a text file and converts its content into a sparse matrix.

    Parameters:
        file_path (str): Path to the text file.

    Returns:
        coo_matrix: Sparse matrix in COO format.
    """
    array = np.loadtxt(file_path, dtype=float)

    rows = array[:, 0].astype(int)
    cols = array[:, 1].astype(int)
    data = array[:, 2]

    n_rows = int(np.max(rows)) + 1
    n_cols = int(np.max(cols)) + 1

    return coo_matrix((data, (rows, cols)), shape=(n_rows, n_cols))
