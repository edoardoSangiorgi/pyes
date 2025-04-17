

def splitter(vector, indices):
    '''
        splits a vector into many parts as the index

        Args:
                vector          :     data to split
                    array-like

                indices         :    index where split
                    tuple
                    list

        Returns:
                tuple of array  :   vector slice after split

        Example:
                In:     [1, 2, 3, 4, 5, 6, 7, 8, 9], [2, 5, 7]
                Out:    [1, 2], [3, 4, 5], [6, 7], [8, 9]
    '''

    if type(indices) == int: indices = [indices]
    if type(indices) == tuple: indices = [index for index in indices]

    indices = [0] + indices + [len(vector)]

    # -- check if the indices are valid --
    if not all(0 <= index <= len(vector) for index in indices):
        raise ValueError('incorrect index value')
    
    # -- vector splitting --
    parts = [vector[indices[i]:indices[i+1]] for i in range(len(indices) - 1)]


    return tuple(parts)