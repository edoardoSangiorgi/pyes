import numpy as np


def to_z_score(data):
    '''
        convert to z-score

        Args:
            dara        :   array of N array with Nf features
                np.array

        Returns:
            np.array    :   z-score data
    '''

    return np.abs((data - np.mean(data)) / np.std(data))