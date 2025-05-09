import os
import mimetypes
from typing import Dict

import pyes.data_io._loaders as loaders
import pyes.data_io._savers as savers


#*## D E T E C T  F I L E  T Y P E #####################################################
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

    if len(type_list) == 1:
        return type_list[0]
    
    return type_list

def _detect_file_type_by_ext(file_path): # tested
    """
        ### Private function - do not use!
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

    EXTENSION_MAP = {
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

    if ext == '':
        ext = None
    elif ext in EXTENSION_MAP:
        return EXTENSION_MAP[ext], ext


    mime, _ = mimetypes.guess_type(file_path)
    if mime:
        guessed_ext = mimetypes.guess_extension(mime) or ext
        return mime, guessed_ext


    return 'application/octet-stream', ext



#*## L O A D E R  F R O M  F I L E ######################################################
def load_from_file(path='', type='auto'):
    '''
        Load data from a file using an appropriate loader based on MIME type.

        Determines the file type automatically or uses the specified type to select
        a loader function from the available handlers. Supports both text-based and
        binary file formats.

        Parameters
        ----------
        path : str, optional
            Path to the file to be loaded. Default is empty string.
        type : str, optional
            MIME type of the file or 'auto' for automatic detection.
            Valid types: 'text/plain', 'text/markdown', 'text/csv', 'application/json',
            'application/xml', 'text/html', 'text/x-python', 'text/x-java-source',
            'text/x-c', 'text/x-c++', 'application/javascript', 'image/jpeg',
            'image/png', 'image/gif', 'application/pdf', 'application/zip',
            'audio/mpeg', 'audio/wav', or 'auto'. Default is 'auto'.

        Returns
        -------
        Any
            Loaded data content. The exact return type depends on the loader used.

        Raises
        ------
        NotImplementedError
            If loader for the specified MIME type is not implemented
        ValueError
            If the specified file type is not supported

        Notes
        -----
        - For unsupported file types, falls back to generic binary loader
        - Image formats (JPEG, PNG, GIF) and some binary formats (PDF, ZIP, audio)
        currently have no implemented loaders and will raise errors

        Examples
        --------
        >>> data = load_from_file('data.csv')
        >>> json_data = load_from_file('config.json', type='application/json')
    '''
    

    LOADERS_MAP = {
        'text/plain': loaders.load_from_textFile,
        'text/markdown': loaders.load_from_textFile,
        'text/csv': loaders.load_from_textFile,
        'application/json': loaders.load_from_textFile, 
        'application/xml': loaders.load_from_textFile,
        'text/html': loaders.load_from_textFile,
        'text/x-python': loaders.load_from_textFile,
        'text/x-java-source': loaders.load_from_textFile,
        'text/x-c': loaders.load_from_textFile,
        'text/x-c++': loaders.load_from_textFile,
        'application/javascript': loaders.load_from_textFile,
        'image/jpeg': None,
        'image/jpeg': None,
        'image/png': None,
        'image/gif': None,
        'application/pdf': None,
        'application/zip': None,
        'audio/mpeg': None,
        'audio/wav': None
    }

    if type == 'auto':
        type = detect_file_type(path)
    else:
        type = type.lower()

    if type in LOADERS_MAP:
        loader = LOADERS_MAP[type]
        if loader is not None:
            return loader(path)
        else:
            raise NotImplementedError(f"Loader for type '{type}' is not implemented.")
    
    return loaders.load_from_binaryFile(path)



#*## S A V E R  T O  F I L E ###########################################################
def save_to_file(data_to_save, file_name, path='', type='auto'):
    '''
        ## ! NOT TESTED YET
        Save data to a file using an appropriate saver based on MIME type.

        Selects the saving method according to the specified file type or uses
        a default text saver for 'auto' detection. Handles both text-based and
        binary file formats.

        Parameters
        ----------
        data_to_save : Any
            Data content to be saved to file. Format must be compatible with
            the selected saver function.
        file_name : str
            Name of the output file (including extension)
        path : str, optional
            Directory path for saving the file. Default is current directory.
        type : str, optional
            MIME type of the file or 'auto' for default text handling.
            Valid types: 'text/plain', 'text/markdown', 'text/csv', 'application/json',
            'application/xml', 'text/html', 'text/x-python', 'text/x-java-source',
            'text/x-c', 'text/x-c++', 'application/javascript', 'image/jpeg',
            'image/png', 'image/gif', 'application/pdf', 'application/zip',
            'audio/mpeg', 'audio/wav', or 'auto'. Default is 'auto'.

        Returns
        -------
        str
            Full path to the saved file

        Raises
        ------
        NotImplementedError
            If saver for the specified MIME type is not implemented
        ValueError
            If the specified file type is not supported

        Notes
        -----
        - The 'auto' type defaults to 'text/plain' handling
        - Image formats (JPEG, PNG, GIF) and some binary formats (PDF, ZIP, audio)
        currently have no implemented savers and will raise errors
        - Unsupported types will fall back to generic binary saving

        Examples
        --------
        >>> save_to_file(df_data, 'output.csv', type='text/csv')
        '/path/to/output.csv'
        >>> save_to_file(config_dict, 'settings.json', type='application/json')
    '''
    
    SAVERS_MAP = {
        'text/plain': savers.save_to_textFile,
        'text/markdown': savers.save_to_textFile,
        'text/csv': savers.save_to_textFile,
        'application/json': savers.save_to_textFile, 
        'application/xml': savers.save_to_textFile,
        'text/html': savers.save_to_textFile,
        'text/x-python': savers.save_to_textFile,
        'text/x-java-source': savers.save_to_textFile,
        'text/x-c': savers.save_to_textFile,
        'text/x-c++': savers.save_to_textFile,
        'application/javascript': savers.save_to_textFile,
        'image/jpeg': None,
        'image/jpeg': None,
        'image/png': None,
        'image/gif': None,
        'application/pdf': None,
        'application/zip': None,
        'audio/mpeg': None,
        'audio/wav': None
    }

    if type == 'auto':
        type = 'text/plain'
    else:
        type = type.lower()

    if type in SAVERS_MAP:
        loader = SAVERS_MAP[type]
        if loader is not None:
            return loader(data_to_save, file_name, path)
        else:
            raise NotImplementedError(f"Saver for type '{type}' is not implemented.")
    
    return savers.save_to_binaryFile(data_to_save, file_name, path)