from typing import List, Union, Optional, Callable
from pathlib import Path

import numpy as np
import keras
import tensorflow as tf

from ..data_io import _loaders
from ..preprocessing.splitting import splitter
from ..data_io.file_manager import detect_file_type 


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
            self.file_type = detect_file_type(data_paths)
        else:
            self.file_type = file_type
        self.normalization_function = normalization

        self._raw_data = None
        self._dataset = None
        self._labels = None

        self._load_functions = {
            'text': _loaders.load_from_textFile,
            'binary': _loaders.load_from_binaryFile
        }
        
        
    #*## L O A D  D A T A ################################################# 
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
    

    #*##  D A T A  P R O C E S S I N G ####################################
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

        labels = self.build_label(split_index)

        all_labels = list(np.concatenate(label_vector) for label_vector in zip(*labels))

        for i in range(len(all_data)):
            all_data[i] = self.normalize(all_data[i])
            all_data[i]= np.reshape(all_data[i], data_shape).astype('float32')

        for i in range(len(all_labels)):
            all_labels[i] = keras.utils.to_categorical(all_labels[i], self.labels)


        return all_data, all_labels


    #*## B U I L D  L A B E L #############################################
    def build_label(self, dimensions):
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
            label = self.build_label(lab_num, dimensions) #TODO: fix using utils.value_to_vector
            lab_num += 1

            label_list.append(label)
        
        return label_list



    def to_tf_dataset(self, input_data, buffer_size=50, batch_size=20):
        '''
            build the dataset for specific data

            Input:
                    input_data:     the data for the dataset
                    array-like 

            Ouput:
                    dataset:        completed dateset
                    tf.Dataset

            Note:
            - *input_data shape must be correct*
            - *labels must be already normalized*
        '''

        if type(input_data) != tuple:
            dataset = tf.data.Dataset.from_tensor_slices((input_data))
        else:
            if len(input_data) != 2: raise ValueError('expected 2 values but ', len(input_data), ' where given')
            data, labels = input_data
            dataset = tf.data.Dataset.from_tensor_slices((data, labels))
        
        self._dataset = dataset.shuffle(buffer_size=buffer_size).batch(batch_size)



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

    
    @property
    def dataset(self):
        if self._dataset == None:
            raise ValueError('No dataset loaded. Call to_tf_dataset() first.')
        
        return self._dataset