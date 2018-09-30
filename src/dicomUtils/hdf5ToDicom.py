import argparse
import h5Convertor
from os import listdir, walk
from os.path import isdir, isfile, join

def readFilesInDir(dirPath):
    return sorted((directoryPath+"/"+f for directoryPath,dirName,files in walk(dirPath) for f in files if isfile(join(dirPath, f))))


def main():
    parser = argparse.ArgumentParser(description='Covert dicom files to hdf5 format')
    parser.add_argument('--i', '--input-dicom', help='path to input DICOM directory')
    parser.add_argument('--h', '--input-hdf5', help='path to input hdf5 file')
    parser.add_argument('--o', '--output-dicom', help='path to output DICOM directory')

    args = parser.parse_args()

    if(args.h.split(".")[-1] != "hdf5"):
        args.h += ".hdf5"

    if(h5Convertor.h5ToDicom(readFilesInDir(args.i), args.h, args.o) < 0):
        print("HDF5 File does not have pixel data in expected format. Expected a dataset with name="+h5h5Convertor.H5_DATASET_NAME)

if __name__ == '__main__':
    main()
