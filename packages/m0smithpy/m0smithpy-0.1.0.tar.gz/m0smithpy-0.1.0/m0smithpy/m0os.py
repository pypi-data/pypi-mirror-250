import json
import os


def makedirsto(file_path, mode=0o777, exist_ok=True):
    """
    Creates all missing directories in the path to a specified file.

    This function checks if the directories in the given file path exist. If not, it creates them.
    It's useful for ensuring that the directory structure for a file exists before performing file operations.

    Parameters:
    - file_path (str): The full file path for which directories need to be created.
      The function extracts the directory path from this file path.
    - mode (int, optional): The mode (permissions) to set for any new directories created.
      Default is 0o777 (octal), which allows read, write, and execute permissions for everyone.
    - exist_ok (bool, optional): If True, an exception will not be raised if the directory already exists.
      If False, an exception will be raised if the directory exists. Default is True.

    Raises:
    - OSError: If the function fails to create the required directories and `exist_ok` is False.

    Example:
    >>> makedirsto('path/to/file.txt')
    This will create the 'path/to' directory if it does not exist.
    """
    dir_path = os.path.dirname(file_path)
    if dir_path and (not exist_ok or not os.path.exists(dir_path)):
        os.makedirs(dir_path, mode, exist_ok)


def m0open(
    file_path,
    mode="r",
    buffering=-1,
    encoding=None,
    errors=None,
    newline=None,
    closefd=True,
    opener=None,
    create_missing_dirs=True,
):
    """
    Opens a file, creating any intermediate directories in the file path if they don't exist.

    This function extends the built-in open function by ensuring that the directory path to the file exists.
    If any directories in the path do not exist, they are created before opening the file.

    Parameters:
    - file_path (str): The path to the file to be opened.
    - mode (str, optional): The mode in which the file is opened. Default is 'r' (read mode).
    - buffering (int, optional): The buffer size used for reading/writing files. Default is -1 (system default).
    - encoding (str, optional): The name of the encoding used to decode or encode the file. This is only applicable in text mode.
    - errors (str, optional): Specifies how encoding/decoding errors are to be handled. This cannot be used in binary mode.
    - newline (str, optional): Controls how universal newlines mode works (it only applies to text mode).
    - closefd (bool, optional): If False, the underlying file descriptor will be kept open when the file is closed. This does not work when a file name is given.
    - opener (callable, optional): A custom opener; must return an open file descriptor.
    - create_missing_dirs (bool, optional): Default True - If True, create any missing folders

    Returns:
    - file object: A file object which can be used to read from and write to the file.

    Raises:
    - OSError: If the function fails to create the required directories or open the file.

    Example:
    >>> with m0open('path/to/file.txt', 'w') as f:
    >>>     f.write('Hello, world!')
    """

    if create_missing_dirs:
        makedirsto(file_path)
    # # Extract the directory path from the file path
    # dir_path = os.path.dirname(file_path)

    # # If the directory path is not empty and does not exist, create it
    # if dir_path and not os.path.exists(dir_path) and :
    #     os.makedirs(dir_path)

    # Open the file with the provided arguments
    return open(file_path, mode, buffering, encoding, errors, newline, closefd, opener)


def spit(data, file_path, append=False):
    """
    Write data to a specified file.

    This function emulates the behavior of Clojure's 'spit' function. It writes the given data to a file at the specified path.
    If the file doesn't exist, it's created. If the file does exist, it's overwritten, unless the 'append' flag is set to True.

    Parameters:
    data (str): The data to be written to the file.
    file_path (str): The path of the file where the data will be written.
    append (bool, optional): If True, the data will be appended to the file if it exists. Defaults to False.

    Returns:
    None
    """
    mode = "w+" if append else "w"
    makedirsto(file_path)
    with open(file_path, mode) as file:
        file.write(data)


def spit_json(data, file_path):
    """
    Write data in JSON format to a specified file.

    This function is designed to serialize Python data structures (e.g., dictionaries, lists) into JSON format and 
    write them to a file. If the file does not exist, it is created. 

    Note: The function assumes that 'data' is serializable to JSON. 

    Parameters:
    data (dict or list): The Python data structure to be serialized into JSON. It must be JSON-serializable.
    file_path (str): The path of the file where the JSON data will be written.
    append (bool, optional): If True, the JSON data will be appended to the file if it exists. Defaults to False.

    Returns:
    None

    Raises:
    TypeError: If the provided data is not serializable into JSON.
    """
    
    makedirsto(file_path)
    with open(file_path, "w") as file:
        json.dump(data, file)
