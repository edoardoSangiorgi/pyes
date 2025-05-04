from typing import List, Union, Optional, Callable
from pathlib import Path

import numpy as np
import keras

from ..data_io import loaders
from ..preprocessing.splitting import splitter
#from pyes.utils import detect_file_type   #! to be tested


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

    """
        Gestione del caricamento e preprocessing di dataset.

        Parameters
        ----------
        data_paths : str or list of str
            Percorsi ai file di dati (raw) da caricare.
        normalization : str or Callable, optional (default='std')
            Funzione o tipo di normalizzazione da applicare ai dati.
        file_type : {'auto', 'text', 'binary'}, optional (default='auto')
            Tipo di file da caricare. Se 'auto', usa 'binary'.

        Attributes
        ----------
        data_paths : list of str
            Lista di percorsi ai file.
        file_type : str
            Tipo di file effettivamente usato ('text' o 'binary').
        normalization_function : Union[str, Callable]
            Funzione di normalizzazione selezionata.
        raw_data : np.ndarray or None
            Dati grezzi caricati; None finché non si chiama `load_data`.
        dataset : Any
            Risultato del preprocessing (non ancora implementato).
        labels : Any
            Etichette generate per il dataset (non ancora implementato).

        Methods
        -------
        load_data()
            Carica i dati raw da file e li memorizza in `raw_data`.
        data_processing(split_index)
            Esegue splitting, creazione etichette e normalizzazione dei dati.
        label_build(dimensions)
            Costruisce la lista di etichette per il dataset.
    """

    def __init__(self, data_paths, normalization='std', file_type='auto' ):
        
        if isinstance(data_paths, str):
            self.data_paths = [data_paths]
        else:
            self.data_paths = data_paths
        if file_type == 'auto':
            self.file_type = 'binary'
        else:
            self.file_type = file_type
        self.normalization_function = normalization

        self._raw_data = None
        self._dataset = None
        self._labels = None

        self._load_functions = {
            'text': loaders.load_from_textFile,
            'binary': loaders.load_from_binaryFile
        }
        
        
        
    def load_data(self):
        '''
            Loads raw data from specified paths.

            Returns
            -------
            loaded_data : list of ndarray
                
        '''

        loaded_data = []
        for file in self.data_paths:
                
            loader = self._load_functions.get(self.file_type)
            loaded_data.append(loader(file))

        self.raw_data = np.array(loaded_data)

        return loaded_data
    


    def data_processing(self, split_index, data_shape):
        '''
            Splitta, crea etichette e normalizza il dataset.

            Parameters
            ----------
            split_index :   int or list of int
                Indici per suddividere i dati in train/val/test.

            data_shape  :   tuple
                the shape of the final data

            Returns
            -------
            None

            Notes
            -----
            - Usa `splitter` per suddividere `raw_data`.
            - `label_build` genera etichette.
            - Applica la normalizzazione a ciascun sottoinsieme.
        '''

        splitted_data = splitter(self.raw_data, split_index)

        all_data = list(np.concatenate(vector) for vector in zip(*splitted_data))

        labels = self.label_build(split_index)

        all_labels = list(np.concatenate(label_vector) for label_vector in zip(*labels))

        for i in range(len(all_data)):
            all_data[i] = self.normalize(all_data[i])
            all_data[i]= np.reshape(all_data[i], data_shape).astype('float32')

        for i in range(len(all_labels)):
            all_labels[i] = keras.utils.to_categorical(all_labels[i], self.num_classes)


        return all_data, all_labels



    def label_build(self, dimensions):
        '''
            Costruisce gli array di etichette per ciascuna classe.

            Parameters
            ----------
            dimensions : int
                Numero di campioni per classe o dimensione del vettore etichetta.

            Returns
            -------
            label_list : list of ndarray
                Lista di array di interi, ciascuno contenente le etichette per una classe.
        '''

        label_list = []
        label = 0
        for _ in self.data_paths:
            label = self.label_build(lab_num, dimensions)
            lab_num += 1

            label_list.append(label)
        
        return label_list



    #############################################################################################*
    #*# P R O P E R T I E S                                                                     #*
    #############################################################################################*

    @property
    def raw_data(self):
        if self._raw_data.all() == None:
            raise AttributeError('No data loaded. Call "load_data()" first. ')
        
        return self._raw_data
    
    @raw_data.setter
    def raw_data(self, new_data):
        self._raw_data = new_data

        
    @property
    def labels(self):
        if self.labels == None:
            raise ValueError('No labels are loaded here!')
        else:
            return self._labels
        
    @labels.setter
    def labels(self, new_labels):
        self._labels = new_labels