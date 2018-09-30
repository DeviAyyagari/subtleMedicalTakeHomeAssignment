import pydicom
import numpy as np
import h5py
import matplotlib.pyplot as plt

H5_DATASET_NAME = "3DVolume"

def dicomToH5(files, outFile):
    h5File = h5py.File(outFile, "w")
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

    dset = h5File.create_dataset(H5_DATASET_NAME, data = dicomArray)
    h5File.close()

    return 0

def h5ToDicom(inputDicomFiles, hdf5File, outputDicomDir):
    sliceLocations = []
    for file in inputDicomFiles:
        dataset = pydicom.dcmread(file)
        sliceLocations.append(dataset.SliceLocation)
    sliceLocations.sort()
    sliceLocationIndeces = {}
    for i,sliceLoc in enumerate(sliceLocations):
        sliceLocationIndeces[sliceLoc] = i
    del sliceLocations[:]

    h5File = h5py.File(hdf5File,'r')

    if H5_DATASET_NAME not in h5File.keys():
        return -1

    dset = h5File[H5_DATASET_NAME]
    array3D = np.array(dset)

    for file in inputDicomFiles:
        dicomFile = pydicom.dcmread(file)
        npArray = array3D[:,:,sliceLocationIndeces[dicomFile.SliceLocation]]
        npArray = npArray * np.linalg.norm(dicomFile.pixel_array)
        npArray = npArray.astype(dicomFile.pixel_array.dtype)
        dicomFile.PixelData = npArray.tobytes()
        dicomFile.save_as(outputDicomDir+"/"+file.split("/")[-1])

    return 0
