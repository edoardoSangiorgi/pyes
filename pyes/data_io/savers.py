import dill

#*### SAVE TO BINARY FILE ########################################################################
def save_to_binaryFile(self, obj, filename, path=''):
    '''
        Save object to a file

        Input:
            obj         :   object to save (e.g. object form class, list, np.array, dict, ...)
            object

            filename    :   file name
            str
                    
            path        :   path where file is saved
            str
        '''

    name = path + filename
    file = open(name, "wb")
    dill.dump( obj, file)  # file
    file.close()

    

#*### SAVE TO TEXT FILE ########################################################################
def save_to_textFile(self, txt, filename, path=''):
    '''
        Save object to file

        Input:
            txt         :   text to save
                object
            filename    :   file name
                str
            
            path        :   path where file is saved
                str
    '''

    with open(path+filename, 'w') as f:
        print(txt, file=f)