import dill

#*### LOAD FROM BINARY FILE ########################################################################
def load_from_binaryFile(filename, path=''):
    '''
        Load object from a binary file

        Input:
            filename    :   file name
            str
                
            path        :   path where file is saved
            str
    '''

    name = path + filename
    file =  open( name, 'rb')
    obj = dill.load(file)
    file.close()

    return obj


#*### LOAD FROM TEXT FILE ########################################################################
def load_from_textFile(filename, path=''):
    '''
        Save object to file

        Input:
            filename    :   file name
            str
                
            path        :   path where file is saved
            str
        '''

    name = path + filename
    file =  open( name, 'r')
    data = file.read()
    file.close()

    return data