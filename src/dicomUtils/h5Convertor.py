import pydicom
import numpy as np
import h5py


def dicomToH5(datasetName,files, outFile):
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
        dicomArray[:,:,sliceLocationIndeces[dataset.SliceLocation]] = dataset.pixel_array
        dicomArray = dicomArray / np.linalg.norm(dicomArray)
    dset = h5File.create_dataset(datasetName, data = dicomArray)
    h5File.close()
