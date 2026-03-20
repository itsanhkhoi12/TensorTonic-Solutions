def min_max_scaling(data):
    """
    Scale each column of the data matrix to the [0, 1] range.
    """
    # Write code here
    def matrix_transpose(A):
        # Write code here
        vector_nums, dims = len(A), len(A[0])
        transposed_A = []
        for i in range(dims):
            transposed_vector = []
            for j in range(vector_nums):
                transposed_vector.append(A[j][i])
            transposed_A.append(transposed_vector)
        
        transposed_row, transposed_col = len(transposed_A), len(transposed_A[0])
        return transposed_A, transposed_row, transposed_col
    
    transposed_data, transposed_row, transposed_col = matrix_transpose(data)
    normalized_transposed_data = []
    for row in transposed_data:
        if len(set(row)) == 1:
            normalized_transposed_data.append([0.0]*transposed_col)
            continue

        normalized_transposed_row = []
        
        for transposed_element in row:
            normalized_element =  (transposed_element - min(row))/ (max(row) - min(row))
            normalized_transposed_row.append(normalized_element)
    
        normalized_transposed_data.append(normalized_transposed_row)

    return matrix_transpose(normalized_transposed_data)[0]