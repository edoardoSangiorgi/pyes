import numpy as np



#*## T O  Z  S C O R E ######################################################
def to_z_score(data): # tested
    '''
        convert to z-score

        Parameters
        ----------
        data    :   array-like
            array of N array with Nf features

        Returns
        -------
        np.array    :   z-score data
    '''

    data = np.array(data)
    return np.abs((data - np.mean(data)) / np.std(data))



#*## I S  E V E N ########################################################### 
def is_even(number): # tested
    '''
        check if a number is even

        Parameters
        ----------
        number  :   int
            the input number, must be int

        Returns
        -------
        boolean :   True if number is even, False if number is odd

        Raises
        ------
        ValueError
            if given number is not int
    '''

    if not isinstance(number, int):
        raise ValueError('number must be int')
    
    if number % 2 == 0:
        return True
    else:
        return False



#*## V A L U E  T O  V E C T O R ############################################
def value_to_vector(value, dimension=None): # tested
    '''
        Create an N-dimensional vector filled with a specified value

        Parameters
        ----------
        value : object
            The value to populate the vector with. Can be of any type.
        dimensions : int or list of int
            List specifying the size of each dimension.
            - Empty list [] returns a 0-dimensional (scalar) value
            - [n] returns a 1D list of length n
            - [n, m] returns a 2D list (n x m matrix)

        Returns
        -------
        nested_list : list
            N-dimensional list structure filled with the specified value.
            The nesting depth equals the length of the dimensions parameter.

    '''
    if not dimension: return value
    if isinstance(dimension, int): dimension = [dimension]
    vector =  [
        value_to_vector(value, dimension[1:]) for _ in range(dimension[0])
    ]
    
    return np.array(vector)




#*### T E S T ########################################################
if __name__ == '__main__':

    val = 5

    print('END', end='\n\n')