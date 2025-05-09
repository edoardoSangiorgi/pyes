import numpy as np

from pyes.utils import is_even



def splitter(data_to_split, split_index='half', axis=0):
    '''
        Splits data into parts at the given indices.

        Parameters
        ----------
        data_to_split   : array-like or int
            Data to split.

        split_index     : tuple, list or int, default = 'half'
            Positions at which to split.
            if default the split index will be the half of the data.
            If the data length is odd, the split index will be the half + 1

        axis     :   int
                dimension where half has to be found

        Returns
        -------
        tuple of arrays
            Vector slices after split.

    '''

    if split_index == 'half':
        split_index = _find_half(data_to_split, axis)

    splitted_data = []
    for data in data_to_split:

        splitted_data.append( _split(data, split_index) )

    return splitted_data



def _split(vector, indices):
    '''
        ### Private function — do not use!

        Splits a vector into parts at the given indices.

        Parameters
        ----------
        vector : array-like or int
            Data to split.

        indices : tuple, list or int
            Positions at which to split.

        Returns
        -------
        tuple of arrays
            Vector slices after split.

        Examples
        --------
        >>> _split([1, 2, 3, 4, 5, 6, 7, 8, 9], [2, 5, 7])
        ([1, 2], [3, 4, 5], [6, 7], [8, 9])
    '''
    
    if isinstance(indices, int): indices = [indices]
    if isinstance(indices, tuple): indices = [index for index in indices]

    indices = [0] + indices + [len(vector)]

    # -- check if the indices are valid --
    if not all(0 <= index <= len(vector) for index in indices):
        raise ValueError('incorrect index value')
    
    # -- vector splitting --
    parts = [vector[indices[i]:indices[i+1]] for i in range(len(indices) - 1)]


    return tuple(parts)



def _find_half(data, axis=0):
    '''
        ### Private function - do no use!
        finds the half of a structure

        Parameters
        ----------
        data    :   array-like
            data which the function finds the half index

        axis     :   int
            dimension where half has to be found

        Returns
        -------
        int     :   the index of the half of the data
                    if the data length is even the index will be the length // 2
                    if the data length is odd the index will be the (length + 1) // 2
    '''

    data = np.array(data)

    if axis >= data.ndim:
        raise ValueError(f"Invalid dimension {axis} for data {data.ndim}D")
    
    data_length = data.shape[axis]

    if data_length == 0:
        raise ValueError('input data is empty')
    

    if is_even(data_length):
        return data_length // 2
    else:
        return (data_length + 1) // 2






#*# T E S T S ########################
if __name__ == '__main__':
     
    vec1 = [1, 2, 3, 4, 5]
    vec2 = [6, 7, 8, 9, 10]

    data = [vec1, vec2]

    
    splitted_data = splitter(data, dim=1)
    print(splitted_data)