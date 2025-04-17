import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler, Normalizer

from utils import to_z_score



#*### MIN - MAX SCALING #################################################################################################
def minmax_scaling(data, min_val = 0, max_val = 1):
    '''
        Scale data to a given range

        Args:
            data        :   array of N array with Nf features
                np.array

            min_val     :   minimum value of the range
                float
                int

            max_val     :   maximum value of the range
                float
                int

        Returns:
            np.array    :   data scaled to the range [min_val, max_val]
    '''
    
    scaler = MinMaxScaler(feature_range=(min_val, max_val))
    return scaler.fit_transform(data)



#*### MAX ABS SCALING #################################################################################################
def maxabs_scaling(data):
    '''
        Scale data in order to have max abs value equal to 1

        Args:
            data        :   array of N array with Nf features
                np.array

        Returns:
            np.array    : scaled data
    '''

    scaler = MaxAbsScaler()
    return scaler.fit_transform(data)



#*### STANDARD SCALING #################################################################################################
def std_norm(data, dim='1D'):
    '''
        Nomalize a list of vector 

        Input:  
            data            :   np.array of N array with Nf features. It can be 1D o 2D
                np.array        input shape (N, dim_x, dim_y)
            
            dim             :   specify the dimension of the input data
        
        Return:
            normalized      :   input data normalized: N vector of Nf features, each with mean=0 and var=1
                np.array
    '''

    scaler = StandardScaler()

    if dim == '1D':
        normalized = scaler.fit_transform(data.T).T
    elif dim == '2D':
        normalized = scaler.fit_transform( data.reshape( (data.shape[0],-1) ).T ).T
        normalized = normalized.reshape(data.shape)
        normalized = np.expand_dims(normalized, axis=3)

    else:
        raise ValueError('Invalid dim. Dim must be "1D" or "2D".')

    return normalized



#*### WHITENING #################################################################################################
def whitening(data):
    '''
        Apply whitening to the data. It makes the data uncorrelated and have unit variance 

        Args:
            data        :   array of N array with Nf features
                np.array

        Returns:
            np.array    :   whitened data
    '''

    mu = data.mean(0)
    sigma = np.cov(data.T)
    evals, evecs = np.linalg.eigh(sigma)
    w = evecs / np.sqrt(evals)
    data = (data - mu) @ w

    return data



#*### NORMALIZATION #################################################################################################
def normalization(data, type_norm='l1'):

    normalizer = Normalizer(norm=type_norm)
    return normalizer.fit_transform(data)



#*### OUTLIER DETECTION ##############################################################################################
def outlier_detection(data, threshold):
    '''
        Detect outliers in the data using z-score method

        Args:
            data        :   array of N array with Nf features
                np.array

            threshold    :   threshold for z-score
                float

        Returns:
            np.array    :   boolean array indicating if the data is an outlier or not
    '''

    z_scores = to_z_score(data)
    return data[z_scores > threshold]



#*### OUTLIER REMOVAL #################################################################################################
def remove_outliers(data, threshold):
    '''
        Remove outliers from the data using z-score method

        Args:
            data        :   array of N array with Nf features
                np.array

            threshold    :   threshold for z-score
                float

        Returns:
            np.array    :   data without outliers
    '''

    z_scores = to_z_score(data)
    return data[z_scores <= threshold]



#*### OUTLIER REPLACEMENT ############################################################################################
def replace_outliers(data, threshold, replacement_value='mean'):
    '''
        Replace outliers in the data using specified method

        Args:
            data            :   array of N array with Nf features
                np.array

            threshold        :   threshold for z-score
                float

            replacement_value:   value to replace the outliers
                float

            method           :   method to use for outlier detection
                str
                'z-score' or 'iqr'

        Returns:
            np.array        :   data with outliers replaced
    '''

    if replacement_value == 'mean': replacement_value = np.mean(data)
    elif replacement_value == 'median': replacement_value = np.median(data)
    
    elif not replacement_value.isnumeric():
        raise ValueError('replacement_value must be numeric, "mean" or "median"')

    
    for el in data:
        if el > threshold:
            el = replacement_value

    return data







#*### T E S T S ###############################################################################################
if __name__ == '__main__':

    np.random.seed(42)  # Per riproducibilità

    # Creazione della matrice di test 10x5
    test_matrix = np.array([
        # Colonna 0: Distribuzione normale (outlier positivo)
        [1.2, 54.1, 0.3, 5.1,    12.3],
        [-0.5, 63.7, 0.7, 6.7,   14.9],
        [2.1, 47.3, 0.1, 7.2,     9.8],
        [0.7, 58.9, 0.9, 100.0,  15.2],   # Outlier colonna 3
        [-1.3, 42.5, 0.5, 4.9,    8.4],
        [1.8, 60.0, 0.2, 5.5,  -200.0],   # Outlier colonna 4
        [0.2, 55.5, 0.8, 6.1,    11.7],
        [-0.9, 49.8, 0.4, 150.0, 10.1],   # Outlier colonna 3
        [1.5, 53.2, 0.6, 5.8,    13.5],
        [2.4, 61.7, 0.3, 6.3,    16.0]
    ])

    

    data = test_matrix
    ans = replace_outliers(data, 0.5, replacement_value='mean')

    print(ans)

    print(ans == data)