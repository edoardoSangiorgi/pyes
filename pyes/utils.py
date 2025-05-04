import os
import mimetypes
from typing import Tuple, Dict

import numpy as np
from pathlib import Path



def to_z_score(data): # tested
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



def detect_file_type(file_paths): # tested
    """
        Detects the MIME type of one or more files based on their extensions.

        Parameters
        ----------
        file_paths : str or list of str
            Path or list of paths to the files to analyze.

        Returns
        -------
        list of str
            List of detected file types (MIME types or simplified labels like 'binary').

        Raises
        ------
        ValueError
            If `file_paths` is empty.

        Notes
        -----
        Files with unknown extensions default to 'application/octet-stream',
        which is then converted to 'binary' for simplicity.
    """

    if not file_paths:
        raise ValueError("File paths cannot be empty")
    
    if isinstance(file_paths, str): file_paths = [file_paths]
        
    
    type_list = []
    for file in file_paths:

        file_type, _ = _detect_file_type_by_ext(file)
        if file_type == 'application/octet-stream': file_type = 'binary'
        type_list.append(file_type)


    return type_list



def _detect_file_type_by_ext(file_path): # tested
    """
        Determines the MIME type of a file based on its extension.

        Parameters
        ----------
        file_path : str
            Path to the file whose MIME type is to be determined.

        Returns
        -------
        tuple of (str or None, str or None)
            - MIME type string if detected, otherwise 'application/octet-stream'.
            - File extension used for detection or guessed by the mimetypes module.

        Notes
        -----
        This function first checks against a predefined extension map.
        If the extension is not found, it attempts to guess using the `mimetypes` module.
    """

    EXTENSION_MAP: Dict[str, str] = {
        '.txt':   'text/plain',
        '.md':    'text/markdown',
        '.csv':   'text/csv',
        '.json':  'application/json',
        '.xml':   'application/xml',
        '.html':  'text/html',
        '.py':    'text/x-python',
        '.java':  'text/x-java-source',
        '.c':     'text/x-c',
        '.cpp':   'text/x-c++',
        '.js':    'application/javascript',
        '.jpg':   'image/jpeg',
        '.jpeg':  'image/jpeg',
        '.png':   'image/png',
        '.gif':   'image/gif',
        '.pdf':   'application/pdf',
        '.zip':   'application/zip',
        '.mp3':   'audio/mpeg',
        '.wav':   'audio/wav',
    }

    _, ext = os.path.splitext(file_path.lower())

    if ext is '':
        ext = None
    elif ext in EXTENSION_MAP:
        return EXTENSION_MAP[ext], ext


    mime, _ = mimetypes.guess_type(file_path)
    if mime:
        guessed_ext = mimetypes.guess_extension(mime) or ext
        return mime, guessed_ext


    return 'application/octet-stream', ext



def is_even(number): # tested
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
    



#*### T E S T ########################################################
if __name__ == '__main__':

    file1 = 'testo.txt'
    file2 = 'binario.bin'

    print('END', end='\n\n')