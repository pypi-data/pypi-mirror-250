import importlib
import os
import socket

from notebook.auth import passwd
from notebook.auth.security import passwd_check


def extension(filename):
    """
    Return extension of a given file. If file has no extension, return None.
    """

    res = filename.split(".")
    if len(res) > 1:
        return res[-1]
    else:
        return None

def list_python_files(project_path):
    """
    List python-related files in a given directory.

    Python-related files are defined as having extenions .py or .ipynb.
    """

    python_ext = ["py", "ipynb"]
    all_files = []

    for rootdir, dirs, files in os.walk(project_path):
        all_files += files
    unique_entries = set(all_files)

    list_of_unique_files = [i for i in unique_entries if extension(i) in python_ext]

    return list_of_unique_files

def listdirs(project_path):
    """
    List directories in a given directory.

    From: https://www.techiedelight.com/list-all-subdirectories-in-directory-python/
    """

    folders = []
    list_of_unique_folders = []

    for rootdir, dirs, files in os.walk(project_path):
        folders += dirs
        # for subdir in dirs:
        #    folders.append(os.path.join(rootdir, subdir))
    unique_entries = set(folders)

    for folder in unique_entries:
        list_of_unique_folders.append(folder)

    return list_of_unique_folders

def hash_password(passwd_string):
    """
    Utility to hash password string.

    It is handy to generate passwords for Jupyter notebooks.
    """

    passwd_input = str(passwd_string)
    
    res = passwd(passwd_input, 'sha1')

    print(passwd_check(res, passwd_input))

    return res

def get_module_installation_path(module):
    """
    Given the name (string) of a module, return the path to location where it is
    installed.
    """

    module = importlib.__import__(module)
    path = os.path.dirname(module.__file__)

    return path

def is_port_free(port, host='localhost'):
    """
    Check if port is open (already allocated) or closed (available).
    """

    # create a new socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        # attempt to connect to the host on the current port
        s.connect((host, port))
        print(f">>> Port {port} is unavailable")
        res = False
    except:
        # if the connection fails, the port is closed
        print(f">>> Port {port} is available")
        res = True
    # always remember to close the socket!
    s.close()
    return res

def find_free_port(lower_bound, upper_bound, host='localhost'):
    """
    Check is a given port is available (closed). If yes, 
    return it. If not, search within a range (`lower_bound`, `upper_bound`) 
    for the next one available and return it.
    """

    # specify the port range to scan
    port_range = range(lower_bound, upper_bound + 1)
    
    # iterate over the port range and check each one
    for port in port_range:
        # create a new socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            # attempt to connect to the host on the current port
            s.connect((host, port))
            # print(f"Port {port} is open")
        except:
            # if the connection fails, the port is closed
            # print(f"Port {port} is available")
            return {'port': port}
        # always remember to close the socket!
        s.close()
    print(f"No ports available in the range ({lower_bound}, {upper_bound})")
    return {'port': port}
