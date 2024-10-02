import wfdb
import os
import pyedflib
import converter as conv
    
# verifies wether the wfdb file at the relative path is valid. It des that by plotting it
def verifyWfdbFile(relative_path):
    try:
        record = wfdb.rdrecord(relative_path)
        annotation = wfdb.rdann(relative_path, 'atr')
        wfdb.plot_wfdb(record=record, annotation=annotation, title='Record with Annotations')
    except Exception as ex:
        print(".wfdb files could not be verified. They might not be valid.")
        print(ex)

#tries to create a wfdb-file from the edf-file and places it in an outp-folder
def writeWfdbFile(record_name, edf_file):
    try:
        conv.write(edf_file=edf_file, wfdbFilePath='./wfdb', record_name=record_name)
    except Exception as ex:
        print(".wfdb files could not be created.")
        print(ex)

# tries to read a edf file at the given path
def readEdfFile(file_path):
    edfFile = None
    try:
        edfFile = pyedflib.EdfReader(file_path)
    except Exception as ex:
        print(".edf file could not be read. Please ensure it is valid.")
        print(ex)
    return edfFile

# input the path to the edf file. Asks until a correct path is given
def inputEdfPath():
    file_path = None
    while True:
        file_path = input("Enter the relative path to the .edf file:")
        if os.path.isfile(file_path) and file_path.endswith(".edf"):
            break
        else:
            print(f".edf File not found at:\t {os.path.abspath(file_path)}")
    return file_path

# input the record name
def inputRecordName():
    record_name = input("Enter the record name:")
    return record_name

def main():    
    file_path = inputEdfPath()
    record_name = inputRecordName()

    edfFile = readEdfFile(file_path)
    writeWfdbFile(record_name, edfFile)
    edfFile.close()
    
    verifyWfdbFile(record_name)
    
main()
