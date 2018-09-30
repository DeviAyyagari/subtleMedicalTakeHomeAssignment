import argparse
import h5Convertor
from os import listdir, walk
from os.path import isdir, isfile, join

def readFilesInDir(dirPath):
    return sorted((directoryPath+"/"+f for directoryPath,dirName,files in walk(dirPath) for f in files if isfile(join(dirPath, f))))


def main():
    parser = argparse.ArgumentParser(description='Covert dicom files to hdf5 format')
    parser.add_argument('--i', '--input-dicom', help='path to input DICOM directory')
    parser.add_argument('--h', '--output-hdf5', help='path to output hdf5 file')

    args = parser.parse_args()

    if(args.h.split(".")[-1] != "hdf5"):
        args.h += ".hdf5"

    h5Convertor.dicomToH5(readFilesInDir(args.i), args.h)

if __name__ == '__main__':
    main()
