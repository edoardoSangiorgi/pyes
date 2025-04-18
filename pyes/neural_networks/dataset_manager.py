from typing import List, Union, Optional, Callable
from pathlib import Path

import numpy as np

from ..data_io import loaders
from ..preprocessing.splitting import split_data
#from ..utils import detect_file_type   #! to be tested



class DatasetManager():

    def __init__(self, data_paths, file_type='auto', normalization=None):
        """
        Args:
            data_paths: Percorsi file o directory, oppure dati in memoria
            file_type: 'text', 'image', 'numpy' o 'auto' per rilevamento automatico
            normalization: Funzione personalizzata per normalizzazione
        """
        self.data_paths = data_paths
        if file_type == 'auto':
            self.file_type = 'binary'
        else:
            self.file_type = file_type
        self.normalization_function = normalization or self.default_normalization
        self.data = None
        self.labels = None
        
        self.load_data()
        
    

    def load_data(self):
        """
        Carica i dati in memoria
        """

        load_function = {
            'text': loaders.load_from_textFile,
            'binary': loaders.load_from_binaryFile
            #'numpy': self.load_numpy
        }
        
        loaded_data = []
        for path in self.data_paths:
                
            loader = load_function.get(self.file_type)
            loaded_data.append(loader(path))
        
        self.data = self._process_loaded_data(loaded_data)


    
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



    