import dill

#*### LOAD FROM BINARY FILE ########################################################################
def load_from_binaryFile(filename, path=''):
    """
        Load a Python object from a binary file using dill.

        Parameters
        ----------
        filename : str
            Name of the binary file.
        path : str, optional
            Directory path where the file is stored. Default is current directory.

        Returns
        -------
        obj : object
            The Python object deserialized from the file.
    """

    full_path = path + filename
    with open(full_path, 'rb') as file:
        obj = dill.load(file)
        
    return obj


#*### LOAD FROM TEXT FILE ########################################################################
def load_from_textFile(filename, path=''):
    """
        Load content from a text file.

        Parameters
        ----------
        filename : str
            Name of the text file.
        path : str, optional
            Directory path where the file is stored. Default is current directory.

        Returns
        -------
        data : str
            The entire contents of the text file.
    """

    full_path = path + filename
    with open(full_path, 'r') as file:
        data = file.read()

    return data
