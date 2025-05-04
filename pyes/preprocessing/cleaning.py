import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler, Normalizer

from ..utils import to_z_score



#*### MIN - MAX SCALING #################################################################################################
def minmax_scaling(data, min_val=0, max_val=1):
    """
        Scale data to a specified range.

        Parameters
        ----------
        data : array-like, shape (n_samples, n_features)
            Input data to be scaled.
        min_val : float or int, optional (default=0)
            Desired lower bound of the transformed data.
        max_val : float or int, optional (default=1)
            Desired upper bound of the transformed data.

        Returns
        -------
        scaled_data : ndarray, shape (n_samples, n_features)
            Transformed data scaled to the interval [min_val, max_val].
    """

    scaler = MinMaxScaler(feature_range=(min_val, max_val))
    return scaler.fit_transform(data)



#*### MAX ABS SCALING #################################################################################################
def maxabs_scaling(data):
    """
        Scale data by its maximum absolute value.

        Parameters
        ----------
        data : array-like, shape (n_samples, n_features)
            Input data to be scaled.

        Returns
        -------
        scaled_data : ndarray, shape (n_samples, n_features)
            Transformed data where each feature is divided by its maximum absolute value.
    """

    scaler = MaxAbsScaler()
    return scaler.fit_transform(data)



#*### STANDARD SCALING #################################################################################################
def std_norm(data, dim='1D'):
    """
        Normalize data to zero mean and unit variance.

        Parameters
        ----------
        data : ndarray
            Input array. Can be 1D or 2D:
            - If dim='1D', data is 1D or 2D with shape (n_features, n_samples).
            - If dim='2D', data is 3D with shape (n_samples, dim_x, dim_y).
        dim : {'1D', '2D'}, optional (default='1D')
            Dimension along which to apply normalization.

        Returns
        -------
        normalized : ndarray
            Normalized data with mean=0 and variance=1 along the specified dimension.

        Raises
        ------
        ValueError
            If `dim` is not '1D' or '2D'.
    """

    scaler = StandardScaler()

    if dim == '1D':
        normalized = scaler.fit_transform(data.T).T
    elif dim == '2D':
        reshaped = data.reshape((data.shape[0], -1))
        normalized_flat = scaler.fit_transform(reshaped.T).T
        normalized = normalized_flat.reshape(data.shape)
        normalized = np.expand_dims(normalized, axis=3)
    else:
        raise ValueError("Invalid dim. Dim must be '1D' or '2D'.")

    return normalized



#*### WHITENING #################################################################################################
def whitening(data):
    """
        Apply whitening transformation to decorrelate features and set unit variance.

        Parameters
        ----------
        data : array-like, shape (n_samples, n_features)
            Input data to whiten.

        Returns
        -------
        whitened_data : ndarray, shape (n_samples, n_features)
            Transformed data with uncorrelated features and unit variance.
    """

    mu = data.mean(axis=0)
    cov = np.cov(data.T)
    evals, evecs = np.linalg.eigh(cov)
    whitening_matrix = evecs / np.sqrt(evals)
    whitened_data = (data - mu) @ whitening_matrix

    return whitened_data



#*### NORMALIZATION #################################################################################################
def normalization(data, type_norm='l1'):
    """
        Normalize samples individually to unit norm.

        Parameters
        ----------
        data : array-like, shape (n_samples, n_features)
            Input data to normalize.
        type_norm : {'l1', 'l2', 'max'}, optional (default='l1')
            Norm to use for normalization.

        Returns
        -------
        normalized_data : ndarray, shape (n_samples, n_features)
            Transformed data where each sample has unit norm.
    """
    normalizer = Normalizer(norm=type_norm)
    return normalizer.fit_transform(data)



#*### OUTLIER DETECTION ##############################################################################################
def outlier_detection(data, threshold, method='std'):
    """
        Detect outliers in the data using specified method.

        Parameters
        ----------
        data : array-like
            Input data for outlier detection.
        threshold : float
            Threshold value for determining outliers.
        method : {'std', 'z-score'}, optional (default='std')
            Method to use for detection:
            - 'std': return values greater than `threshold`.
            - 'z-score': compute z-scores and return values with |z| >= `threshold`.

        Returns
        -------
        outliers : ndarray
            Array of detected outlier values.
    """
    if method == 'std':
        return data[data > threshold]
    elif method == 'z-score':
        z_scores = to_z_score(data)
        return data[z_scores >= threshold]
    else:
        raise ValueError("Invalid method. Choose 'std' or 'z-score'.")



#*### OUTLIER REMOVAL #################################################################################################
def remove_outliers(data, threshold, method='std'):
    """
        Remove outliers from the data using specified method.

        Parameters
        ----------
        data : array-like
            Input data from which to remove outliers.
        threshold : float
            Threshold value for determining outliers.
        method : {'std', 'z-score'}, optional (default='std')
            Method to use for removal:
            - 'std': remove values greater than `threshold`.
            - 'z-score': compute z-scores and remove values with |z| > `threshold`.

        Returns
        -------
        cleaned_data : ndarray
            Data with outliers removed.
    """
    if method == 'std':
        return data[data < threshold]
    elif method == 'z-score':
        z_scores = to_z_score(data)
        return data[z_scores <= threshold]
    else:
        raise ValueError("Invalid method. Choose 'std' or 'z-score'.")



#*### OUTLIER REPLACEMENT ############################################################################################
def replace_outliers(data, threshold, replacement_value='mean'):
    """
        Replace outliers in the data with a specified value.

        Parameters
        ----------
        data : array-like
            Input data containing potential outliers.
        threshold : float
            Threshold for determining outliers (values > threshold are replaced).
        replacement_value : {'mean', 'median'} or float, optional (default='mean')
            Value to replace outliers:
            - 'mean': global mean of `data`.
            - 'median': global median of `data`.
            - float: specified constant value.

        Returns
        -------
        replaced_data : ndarray
            Data with outliers replaced.

        Raises
        ------
        ValueError
            If `replacement_value` is not 'mean', 'median', or numeric.
    """

    if replacement_value == 'mean':
        replacement_value = np.mean(data)
    elif replacement_value == 'median':
        replacement_value = np.median(data)
    elif not isinstance(replacement_value, (int, float)):
        raise ValueError("replacement_value must be numeric, 'mean', or 'median'.")

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
    