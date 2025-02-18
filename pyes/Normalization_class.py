from FilesManager_class import FilesManager
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler


class Normalization():

    def __init__(self):
        self.obj_LabelEncoder = preprocessing.LabelEncoder()

        self.scaler = StandardScaler()
        
        #   Model
        self.fashion_model  = None   
        self.loadedModel    = None
        
        #   Fit result 
        self.fit_result = None

        self.filesManager = FilesManager()


    #   1 D - N O R M A L I Z A T I O N     ----------------------------------------------------------------------------------------------------------------------------------------------------------------
    def vector1DNormalization(self, data):
        '''
            Nomalize a list of vector 

            Input:  
                data            :   np.array of N array with Nf features 
                    np.array        input shape (N, dim_x, dim_y)
            
            Return:
                normalized      :   input data normalized: N vector of Nf features, each with mean=0 and var=1
                    np.array
        '''
        normalized = self.scaler.fit_transform(data.T).T

        return normalized
    

    #   2 D - N O R M A L I Z A T I O N     ----------------------------------------------------------------------------------------------------------------------------------------------------------------
    def image2DNormalization(self, data):
        '''
            Normalize 2D image. From (N, dim_x, dim_y) to (N, dim_x, dim_y, 1) where each image i in N has mean=0 and var=1

            Input:
                data            :   np.array of N image with shape (dim_x, dim_y))
                    np.array        input shape (N, dim_x, dim_y)

            Return:
                normalized      :   input data normalized: N images of shape (dim_x, dim_y, 1) each with mean=0 and var=1
                    np.array
        '''
        normalized = self.scaler.fit_transform( data.reshape( (data.shape[0],-1) ).T ).T
        normalized = normalized.reshape(data.shape)
        normalized = np.expand_dims(normalized, axis=3)

        return normalized