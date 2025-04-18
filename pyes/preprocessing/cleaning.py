import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler, Normalizer

from ..utils import to_z_score




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
def outlier_detection(data, threshold, method='std'):
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

    outlier = data.copy()
    if method == 'std':
        return outlier[outlier > threshold]
    elif method == 'z-score':
        z_scores = to_z_score(data)
        return outlier[z_scores >= threshold]



#*### OUTLIER REMOVAL #################################################################################################
def remove_outliers(data, threshold, method='std'):
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

    cleaned_data = data.copy()
    if method == 'std':
        return cleaned_data[cleaned_data < threshold]
    elif method == 'z-score':
        z_scores = to_z_score(data)
        return cleaned_data[z_scores <= threshold]



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

        Returns:
            np.array        :   data with outliers replaced
    '''

    if replacement_value == 'mean': replacement_value = np.mean(data)
    elif replacement_value == 'median': replacement_value = np.median(data)
    
    elif not type(replacement_value) in [int, float]:
        raise ValueError('replacement_value must be numeric, "mean" or "median"')

    ## Replacement method
    cleaned_data = data.copy() 
    cleaned_data[cleaned_data > threshold] = replacement_value

    return cleaned_data







#*### T E S T S ###############################################################################################
if __name__ == '__main__':

    vector = np.array([[[1, 3], [5, 12]], [[3, 5], [25, 8]]])
    soglia = 10
    sostituto = 10

    print(replace_outliers(vector, soglia, replacement_value='mean'))
    print(remove_outliers(vector, soglia))
    print(outlier_detection(vector, soglia))
    