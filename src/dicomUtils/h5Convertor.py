import pydicom
import numpy as np
import h5py
from os import listdir, walk
from os.path import isdir, isfile, join

H5_DATASET_NAME = "3DVolume"

def readFilesInDir(dirPath):
    """
    Return files in the given directory
    """
    return sorted((directoryPath+"/"+f for directoryPath,dirName,files in walk(dirPath) for f in files if isfile(join(dirPath, f))))


def dicomTo3DVolume(dicomInputPath, **kwargs):
    """
    Take a dicomInputPath to one Dicom image set and return a 3DVolume 
    **kwargs are to support this function as an allDicomOps op
    """
    files = readFilesInDir(dicomInputPath)
    refDs = pydicom.dcmread(files[0])
    dicomArray = np.zeros((int(refDs.Rows), int(refDs.Columns), len(files)), dtype=np.float32)

    sliceLocations = []
    for file in files:
        dataset = pydicom.dcmread(file)
        sliceLocations.append(dataset.SliceLocation)
    sliceLocations.sort()
    sliceLocationIndeces = {}
    for i,sliceLoc in enumerate(sliceLocations):
        sliceLocationIndeces[sliceLoc] = i
    del sliceLocations[:]

    for file in files:
        dataset = pydicom.dcmread(file)
        dicomArray[:,:,sliceLocationIndeces[dataset.SliceLocation]] = dataset.pixel_array/np.linalg.norm(dataset.pixel_array)

    return dicomArray

def write3DVolumeToH5(dicomArray, outFile):
    h5File = h5py.File(outFile, "w")

    dset = h5File.create_dataset(H5_DATASET_NAME, data = dicomArray)
    h5File.close()


def dicomToH5(dicomInputPath, outFile):
    array3D = dicomTo3DVolume(dicomInputPath)
    write3DVolumeToH5(array3D, outFile)

def h5ToDicom(dicomInputPath, hdf5File, outputDicomDir):
    array3D = readVolumeFromH5File(hdf5File)
    if(array3D is None):
        return False
    volume3DToDicom(dicomInputPath, array3D, outputDicomDir)
    return True

def readVolumeFromH5File(hdf5File):
    h5File = h5py.File(hdf5File,'r')

    if H5_DATASET_NAME not in h5File.keys():
        return None

    dset = h5File[H5_DATASET_NAME]
    return np.array(dset)

def volume3DToDicom(dicomInputPath, array3D, outputDicomDir):
    inputDicomFiles = readFilesInDir(dicomInputPath)
    sliceLocations = []
    for file in inputDicomFiles:
        dataset = pydicom.dcmread(file)
        sliceLocations.append(dataset.SliceLocation)
    sliceLocations.sort()
    sliceLocationIndeces = {}
    for i,sliceLoc in enumerate(sliceLocations):
        sliceLocationIndeces[sliceLoc] = i
    del sliceLocations[:]

    for file in inputDicomFiles:
        dicomFile = pydicom.dcmread(file)
        npArray = array3D[:,:,sliceLocationIndeces[dicomFile.SliceLocation]]
        npArray = npArray * np.linalg.norm(dicomFile.pixel_array)
        npArray = npArray.astype(dicomFile.pixel_array.dtype)
        dicomFile.PixelData = npArray.tobytes()
        dicomFile.save_as(outputDicomDir+"/"+file.split("/")[-1])
