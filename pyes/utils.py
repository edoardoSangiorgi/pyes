import numpy as np
from pathlib import Path


def to_z_score(data):
    '''
        convert to z-score

        Parameters
        ----------
        data    :   array-like
            array of N array with Nf features

        Returns
        -------
        np.array    :   z-score data
    '''

    data = np.array(data)
    return np.abs((data - np.mean(data)) / np.std(data))



def detect_file_type(file_paths):
    """
        ## #! TO BE TESTED
        Rileva e verifica il tipo di file coerente da una lista di percorsi
        
        Args:
            file_paths: Lista di percorsi a file da analizzare
            
        Returns:
            Tipo di file comune a tutti i percorsi (text, image, numpy, o unknown)
            
        Raises:
            ValueError: Se vengono rilevati tipi misti o percorsi non validi
    """

    if not file_paths:
        raise ValueError("File paths cannot be empty")
        
    
    EXTENSION_MAP = {
        'text': {'.txt', '.csv', '.tsv', '.json'},
        'binary': {'.bin', '.dat'},
        'image': {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff'},
        'numpy': {'.npy', '.npz'},
        'audio': {'.wav', '.mp3', '.flac'},
        'video': {'.mp4', '.avi', '.mov'}
    }
    
    # Inversione della mappatura per lookup veloce
    TYPE_FROM_EXT = {ext: ftype for ftype, exts in EXTENSION_MAP.items() for ext in exts}
    
    detected_type = None
    
    for file_path in file_paths:

        if not Path(file_path).exists():
            raise FileNotFoundError(f"The file {file_path} don't exist")
            
        ext = Path(file_path).suffix.lower()
        if not ext:
            raise ValueError(f"File without extension: {file_path}")
        
        file_type = TYPE_FROM_EXT.get(ext, 'unknown')
        
        if detected_type is None:
            detected_type = file_type
            if file_type == 'unknown':
                raise ValueError(f"Type not supported: {ext} in {file_path}")
        elif file_type != detected_type:
            raise ValueError(f"Mixing file types: {detected_type} e {file_type} in {file_path}")
    
    return detected_type



def is_even(number):
    '''
        check if a number is even

        Parameters
        ----------
        number  :   int
            the input number, must be int

        Returns
        -------
        boolean :   True if number is even, False if number is odd

        Raises
        ------
        ValueError
            if given number is not int
    '''

    if not isinstance(number, int):
        raise ValueError('number must be int')
    
    if number % 2 == 0:
        return True
    else:
        return False