from typing import List, Union, Optional, Callable
from pathlib import Path

import numpy as np

from ..data_io import loaders
from ..preprocessing.splitting import split_data
#from ..utils import detect_file_type   #! to be tested


'''
DOCS:

Funzionalità:
- load data     :    caricare dati grezzi, sia parziali che completi    OK
- load dataset  :    caricare il dataset completo processato
- load class    :    caricare una singola classe (parte del dataset)
- split data    :    suddividere il dataset

- process data  :   fa il preprocessing del dataset
    - creare le labels
    - accoppiare dati - labels
    - normalizzazione

'''


class DatasetManager():

    def __init__(self, data_paths, normalization, file_type='auto' ):
        """
        Args:
            data_paths      :   file paths to the data
            list or str

            file_type:      :   type of the file
            str
                            :   'text'
                            :   'binary'
                            :   'auto' (default) #! automatically set binary for now
                            
            normalization:  :   normalization function
            str
        """
        self.data_paths = data_paths
        if file_type == 'auto':
            self.file_type = 'binary'
        else:
            self.file_type = file_type
        self.normalization_function = normalization

        self._data = None
        self._dataset = None
        self._labels = None
        
        
    

    def load_dataset(self):
        """
            Load the entire datset
        """
        
        self._dataset = self._process_loaded_data(self.data)


    
    def split_data(self, test_size=0.2, val_size=None, random_state= None):
        """
        Split dati in train/val/test
        Restituisce tuple di array (train, val, test) o (train, test)
        """
        
        from sklearn.model_selection import train_test_split
        
        if val_size:
            val_size = val_size / (1 - test_size)  # Corregge il ratio per split annidato
            train_val, test = train_test_split(
                self.data, test_size=test_size, random_state=random_state)
            train, val = train_test_split(
                train_val, test_size=val_size, random_state=random_state)
            return (train, val, test)
        
        return train_test_split(self.data, test_size=test_size, random_state=random_state)



    
    def _process_loaded_data(self, raw_data):
        """
        Processamento base per dati caricati
        """

        # Converti liste e formati diversi in numpy array
        processed = [np.array(d) for d in raw_data]
        
        # Uniforma le dimensioni aggiungendo dimensioni singleton se necessario
        max_dim = max(arr.ndim for arr in processed)
        for i, arr in enumerate(processed):
            if arr.ndim < max_dim:
                processed[i] = np.expand_dims(arr, axis=-1)
        
        return np.concatenate(processed, axis=0)

    # - # - # - # – # – # – # – # – # – # – # – # – # – # – # – # – # – # – # – # – # – # – # – # – # –

    def load_data(self):
        '''
            load raw data from specified file
        '''

        load_functions = {
            'text': loaders.load_from_textFile,
            'binary': loaders.load_from_binaryFile
        }

        loaded_data = []
        for file in self.data_paths:
                
            loader = load_functions.get(self.file_type)
            loaded_data.append(loader(file))

        self.data = loaded_data

        return loaded_data
    

    def data_processing(self):
        '''
            - label creation
            - coupling data - labels
            - normalizing
        '''

        #TODO: contitnua qui!


        



    #############################################################################################
    ## P R O P E R T I E S                                                                      #
    #############################################################################################

    @property
    def data(self):
        if self._data == None:
            raise AttributeError('No data loaded. Call "load_data()" first. ')
        
        return self._data
        
    @property
    def labels(self):
        if self.labels == None:
            raise ValueError('No labels are loaded here!')
        else:
            return self._labels
    