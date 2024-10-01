import wfdb
import numpy as np
import os
import wfdb
import pyedflib
    
def write(edfFile : pyedflib.edfreader.EdfReader, wfdbFilePath, recordName):
    
    print(f"Full File Path {os.path.abspath(wfdbFilePath)}")
    
    # create the dir, and move to it 
    os.makedirs(wfdbFilePath, exist_ok=True)
    os.chdir(wfdbFilePath)
    
    _units = []
    _sigNames = []
    _gain = []
    _signals = []
    _fmt = []
    _baseline = []
    for n in range(edfFile.signals_in_file):
        _units.append(edfFile.getPhysicalDimension(n))
        _sigNames.append(edfFile.getSignalLabels()[n])
        _signals.append(edfFile.readSignal(n))
        
        _fmt.append('16')
        _baseline.append(0)
        
        n_gain = (edfFile.getPhysicalMaximum(0) - edfFile.getPhysicalMinimum(0)) / (edfFile.getDigitalMaximum(0) - edfFile.getDigitalMinimum(0))
        _gain.append(n_gain)
    
    _signals = np.array(_signals).T
    
    # create the wfdb header
    wfdb.wrsamp(record_name=recordName,
        fs=edfFile.samplefrequency(0),   # Sampling frequency
        units=_units,                    # Units for each channel
        sig_name=_sigNames,              # Signal names
        p_signal=_signals,               # Signal data (physical)
        adc_gain=_gain,                  # gain
        baseline=_baseline,              # assumed to be 0 for this exercise
        fmt=_fmt                         # fmt is standardiced for edf files
    )             
    
    _ann = edfFile.readAnnotations()
    
    # Write the annotation file
    wfdb.wrann(record_name=recordName,
        extension='atr',                # Annotation file extension
        sample=_ann[0].astype(int),     # Sample indices for annotations
        symbol=np.array(['A', 'B']))#_ann[2])                   # Symbols for annotations (TODO: make sure the full labels are used)
    


################# verify 

def verify(fullPath):
    record = wfdb.rdrecord(fullPath)

    # Read and display the annotations
    annotation = wfdb.rdann(fullPath, 'atr')
    wfdb.plot_wfdb(record=record, annotation=annotation, title='Example Record with Annotations')
