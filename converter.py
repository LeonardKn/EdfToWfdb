
import wfdb
import numpy as np
import os
import pyedflib

def write(edf_file : pyedflib.edfreader.EdfReader, wfdbFilePath, record_name):
    # create the dir, and move to it 
    os.makedirs(wfdbFilePath, exist_ok=True)
    os.chdir(wfdbFilePath)
    
    createHeaAndDatFiles(edf_file, record_name)             
    createAnnotationFile(edf_file=edf_file, record_name=record_name)
    
# creates the annotation-file containing info about points of interest
def createAnnotationFile(edf_file: pyedflib.edfreader.EdfReader, record_name):
    _sample = getSampleIndexes(edf_file)
    
    wfdb.wrann(record_name=record_name,
        extension='atr',                # Annotation file extension
        sample=_sample,                 # Sample indices for annotations
        symbol=np.array(['A', 'B']))    #_ann[2])                   # Symbols for annotations (TODO: make sure the full labels are used).

def getSampleIndexes(edf_file):
    sample_number = edf_file.samplefrequency(0) * edf_file.getFileDuration()
    _ann = edf_file.readAnnotations()
    _sample = []
    
    #since the annotation positions are stored in seconds in edf and samples in wfdb
    for s in _ann[0]:
        sample_index = s * edf_file.samplefrequency(0)
        sample_index = max(0, min(sample_index, sample_number-1))       #TODO: do we want to keep this -1? Its necessary for the veryfyer to read the file
        _sample.append(sample_index)
    
    _sample = np.array(_sample).astype(int)
    return _sample  
    
# creates the header and data file with the values of the passed edf file
def createHeaAndDatFiles(edf_file : pyedflib.edfreader.EdfReader, record_name):
    _units, _sigNames, _gain, _signals, _fmt, _baseline = [], [], [], [], [], []
    fillHeaArrays(edf_file, _units, _sigNames, _gain, _signals, _fmt, _baseline)
    
    _signals = np.array(_signals).T
    
    # create the wfdb header
    wfdb.wrsamp(record_name=record_name,
        fs=edf_file.samplefrequency(0),   # Sampling frequency
        units=_units,                    # Units for each channel
        sig_name=_sigNames,              # Signal names
        p_signal=_signals,               # Signal data (physical)
        adc_gain=_gain,                  # gain
        baseline=_baseline,              # assumed to be 0 for this exercise
        fmt=_fmt                         # fmt is standardiced for edf files
    )

# fills the data-arrays with the the values of the edf file. These arrays will be used to to create the wfdb file
def fillHeaArrays(edf_file, _units, _sigNames, _gain, _signals, _fmt, _baseline):
    for n in range(edf_file.signals_in_file):
        _units.append(edf_file.getPhysicalDimension(n))
        _sigNames.append(edf_file.getSignalLabels()[n])
        _signals.append(edf_file.readSignal(n))
        
        _fmt.append('16')
        _baseline.append(0)
        
        n_gain = (edf_file.getPhysicalMaximum(0) - edf_file.getPhysicalMinimum(0)) / (edf_file.getDigitalMaximum(0) - edf_file.getDigitalMinimum(0))
        _gain.append(n_gain)#_ann[2])                   # Symbols for annotations (TODO: make sure the full labels are used).
    
