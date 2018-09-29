import pydicom
from os import listdir
from os.path import isfile, join

def readFilesInDir(dirPath):
    return [f for f in listdir(dirPath) if isfile(join(dirPath, f))]

def dicomToH5(fileName):
    pydicom.dcmread(fileName)
    pass
