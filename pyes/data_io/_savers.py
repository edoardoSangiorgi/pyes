import dill

#*### SAVE TO BINARY FILE ########################################################################
def save_to_binaryFile(obj, filename, path=''):
    """
        Serialize and save a Python object to a binary file using dill.

        Parameters
        ----------
        obj : object
            Python object to serialize (e.g. istanza di classe, list, np.array, dict, …).
        filename : str
            Name of the target binary file.
        path : str, optional
            Directory path in cui salvare il file. Default è la directory corrente.

        Returns
        -------
        None
    """
    full_path = path + filename
    with open(full_path, "wb") as file:
        dill.dump(obj, file)


#*### SAVE TO TEXT FILE ########################################################################
def save_to_textFile(txt, filename, path=''):
    """
        Save a text string to a plain-text file.

        Parameters
        ----------
        txt : str
            Contenuto testuale da salvare nel file.
        filename : str
            Nome del file di destinazione.
        path : str, optional
            Directory path in cui salvare il file. Default è la directory corrente.

        Returns
        -------
        None
    """
    full_path = path + filename
    with open(full_path, "w") as file:
        file.write(txt)
