import pyedflib
import numpy as np
import os.path


def read(fpath):
    print(f"Full File Path {os.path.abspath(fpath)}")
    
    if os.path.isfile(fpath):
        print(f" {fpath} exists\n")

    # Open the EDF file
    edf_file = pyedflib.EdfReader(fpath)
    
    return edf_file
    