import os
import hashlib

def get_list_of_files_from(dirname):
    """_summary_

    Args:
        dir (_type_): _description_

    Returns:
        _type_: _description_
    """
    files, subfolders = [], []

    for f in os.scandir(dirname):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            files.append(f.path)

    for subfolder in list(subfolders):
        f, sf = get_list_of_files_from(subfolder)
        subfolders.extend(sf)
        files.extend(f)

    return files, subfolders

def get_list_of_files_from_ext(dirname, extension):
    # Function to get all CSV files from the root folder and its subdirectories
    files, subfolders = [], []

    for f in os.scandir(dirname):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            if str.lower(os.path.splitext(f)[1][1:]) == extension:
                files.append(f.path)

    for subfolder in list(subfolders):
        f, sf = get_list_of_files_from_ext(subfolder, extension)
        subfolders.extend(sf)
        files.extend(f)

    return files, subfolders

def create_md5_hash(string):
    """Creates an MD5 hash from a given string.

    Args:
    string: The string to hash.

    Returns:
    The MD5 hash of the string in hexadecimal format.
    """

    # Encode the string as UTF-8 bytes
    encoded_string = string.encode('utf-8')

    # Create an MD5 hash object
    md5_hash = hashlib.md5()

    # Update the hash object with the encoded string
    md5_hash.update(encoded_string)

    # Get the hexadecimal representation of the hash
    hash_hex = md5_hash.hexdigest()

    return hash_hex
