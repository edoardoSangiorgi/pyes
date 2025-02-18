from FilesManager_class import FilesManager
import numpy as np
import keras
import tensorflow as tf
from Normalization_class import Normalization


class DataProcessing():


    def __init__(self, file_path_list, file_type = 'text'):


        self.num_classes = len(file_path_list)

        filesManager = FilesManager()
        self.normalizer = Normalization()

        self.files_list = []
        for path in file_path_list:
            if file_type == 'bin':
                file = filesManager.load_from_binaryFile(path)
            elif file_type == 'text':
                file = filesManager.load_from_textFile(path)

            self.files_list.append(file)



    ###  M A I N  M E T H O D S  ######################################################################################

    def load_dataset(self, split_index):
        '''
            ### This is for all classes
            Load the entire dataset

            Input:
                    split_index     :   index or indeces for splitting data
                        list
                        tuple
                        int

            Output:
                    (data1, label1) ... (dataN, labelN)
        '''

        all_data, all_labels = self.build_data(split_index)
        '''
            - data are in the correct shape
            - labels are already normalized
        '''

        dataset = []
        for (data, label) in zip(all_data, all_labels):
            dataset.append(self.build_dataset((data, label)))

        return tuple(dataset)
    

    def load_data(self, split_index):
        '''
            ### This is for all classes
            split all the data into N parts:  the splitting is computed for each class


            The output is ALREADY NORMALIZED

            Input:
                    split_index:    the index for the splitting
                    - int
                    - tuple of int
            
            Output:
                    (train_data, train_labels):     the first part of the data with the labels
                        tuple of array

                    (val_data, val_labels):         the second part of the data with the labels
                        tuple of array

                    (test_data, test_labels):       the thirs part of the data (not computed here but taken as class variable)
                        tuple of array
        '''

        
        all_data, all_labels = self.build_data(split_index)

        # -- reshaping all the data in the form: (data1, labels1), ... (dataN, labelsN)
        return_data = []
        for (data, label) in zip(all_data, all_labels):
            return_data.append((data, label))


        return tuple(return_data)




    def build_dataset(self, input_data, buffer_size=50, batch_size=20):
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
        
        dataset = dataset.shuffle(buffer_size=buffer_size).batch(batch_size)

        return dataset
    

    def build_data(self, split_index):
        '''
            operations list:
            - split data and rearanging
            - split labels and rearanging
            - normalization and reshape (-1, 3840, 1) in float32
            - one hot encoding of labels

            Input:
                    split_index:    a set of index used to split both the data and the lables
                    [int, int ...]
                    int

            Output:
                    all_data, all_lables
                    tuple, tuple 

        '''

        splitted_data = self.split_all(split_index)
        '''
            possibile shape of splitted data:
                - (data1_train, data1_test), (data2_train, data2_test) ...
                - (data1_train, data1_val, data1_test), (data2_train, data2_val, data2_test) ...
        '''

        all_data = list(np.concatenate(vector) for vector in zip(*splitted_data))
        '''
            put all the train/val/test data together
            possibile result:
                - (data_train, data_test)
                - (data_train, data_val, data_test)
        '''

        all_generated_labels = self.build_all_labels(split_index)
        '''
            possibile shape of all_labels
                - (data1_labels_train, data1_labels_test), (data2_labels_train, data2_labels_test)
                - (data1_labels_train, data1_labels_val, data1_labels_test), (data2_labels_train, data2_labels_val, data2_labels_test)
        '''

        all_labels = list(np.concatenate(label_vector) for label_vector in zip(*all_generated_labels))
        '''
            possible results:
                - (labels_train, labels_test)
                - (labels_train, labels_val, labels_test)
        '''

        for i in range(len(all_data)):        
            all_data[i] = self.normalize(all_data[i])
            all_data[i]= np.reshape(all_data[i], (-1, 3840, 1)).astype('float32')

        for i in range(len(all_labels)):
            all_labels[i] = keras.utils.to_categorical(all_labels[i], self.num_classes)


        return all_data, all_labels


    ### S T A N D  A L O N E  M E T H O D S  ########################################################################

    def load_class(self, class_to_load):

        if class_to_load > self.num_classes:
            raise ValueError('invalid class')
        else:
            return self.files_list[class_to_load]


    def build_all_labels(self, dimensions):

        label_list = []
        lab_num = 0
        for data in self.files_list:
            label = self.label_build(lab_num, dimensions)
            lab_num += 1

            label_list.append(label)
        
        return label_list
    

    def label_build(self, value, dimensions, max_dim = 100):

        vector = [value] * max_dim
        vectors = self.splitter(vector, dimensions)

        return tuple(vectors)


    def split_all(self, split_index):
        clutter_splitted = self.splitter(self.clutter, split_index)
        falling_splitted = self.splitter(self.falling, split_index)
        moving_arm_splitted = self.splitter(self.moving_arm, split_index)
        target_presence_splitted = self.splitter(self.target_presence, split_index)

        return clutter_splitted, falling_splitted, moving_arm_splitted, target_presence_splitted


    def load_examples(self):
        return self.clutter[0], self.falling[0], self.moving_arm[0], self.target_presence[0]


    def load_class_example(self, class_to_load):

        # -- clutter --
        if class_to_load == 0:
            return self.clutter[0]
        
        # -- falling ---
        elif class_to_load == 1:
            return self.falling[0]
        
        # --- moving arm ---
        elif class_to_load == 2:
            return self.moving_arm[0]
        
        # --- target presence ---
        elif class_to_load == 3:
            return self.target_presence[0]
        
        else:
            return None



    ###  U T I L S  ##########################################################################################À


    def normalize(self, data, interval=None):
        if interval == None:
            return self.normalizer.vector1DNormalization(data)
        
        elif interval == '0-1':
            return (data - np.min(data)) / (np.max(data) - np.min(data))
        
        else: raise ValueError('invalid interval')
    


    def splitter(self, vector, indices):
        '''
            splits a vector into many parts as the index

            Input:
                    vector          :     data to split
                        array-like

                    indices         :    index where split
                        tuple
                        list

            Ouput:
                    tuple of array  :   vector slice after split

            Example:
                    In:     [1, 2, 3, 4, 5, 6, 7, 8, 9], [2, 5, 7]
                    Out:    [1, 2], [3, 4, 5], [6, 7], [8, 9]
        '''

        if type(indices) == int: indices = [indices]
        if type(indices) == tuple: indices = [index for index in indices]

        indices = [0] + indices + [len(vector)]
    
        # -- check if the indexes are valid --
        if not all(0 <= index <= len(vector) for index in indices):
            raise ValueError('incorrect index value')
        
        # -- vector splitting --
        parts = [vector[indices[i]:indices[i+1]] for i in range(len(indices) - 1)]
    

        return tuple(parts)

                
                

###  T E S T  ###############################################################################################
if __name__ == '__main__':

    loader = DataProcessing()

    vector = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    indices = (2, 5, 7)
    part1, part2, part3, part4 = loader.splitter(vector, indices)
    print(part1)
    print(part2)
    print(part3)
    print(part4)

    (data1, label1), (data2, label2) = loader.load_data(50)
    print('done')