import numpy as np

def matrix_normalization(matrix, axis=None, norm_type='l2'):
    """
    Normalize a 2D matrix along specified axis using specified norm.
    """
    # Write code here

    norm_type_standards = ['l2','l1','max']
    norm_type = norm_type.lower()
    matrix = np.array(matrix)

    if norm_type not in norm_type_standards:
        return None
    if matrix.ndim != 2:
        return None
    if matrix.size == 0:
        return None
    if axis not in (None, 0, 1):
        return None
        
    else:
        if norm_type == 'l2':
            l2_norm = np.sqrt(np.sum(np.square(matrix),axis=axis,keepdims = True))
            return np.where(l2_norm == 0, 0,matrix/l2_norm)
            
        elif norm_type == 'l1':
            l1_norm = np.sum(np.abs(matrix),axis = axis, keepdims=True)
            return np.where(l1_norm == 0, 0,matrix/l1_norm)

        else:
            max_norm = np.max(np.abs(matrix),axis=axis, keepdims = True)
            return np.where(max_norm == 0, 0, matrix/max_norm)
