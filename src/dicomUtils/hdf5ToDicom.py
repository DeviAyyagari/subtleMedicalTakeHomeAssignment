import argparse
import h5Convertor

def main():
    parser = argparse.ArgumentParser(description='Covert dicom files to hdf5 format')
    parser.add_argument('--i', '--input-dicom', help='path to input DICOM directory')
    parser.add_argument('--h', '--input-hdf5', help='path to input hdf5 file')
    parser.add_argument('--o', '--output-dicom', help='path to output DICOM directory')

    args = parser.parse_args()

    if(args.h.split(".")[-1] != "hdf5"):
        args.h += ".hdf5"

    if(not h5Convertor.h5ToDicom(args.i, args.h, args.o)):
        print("HDF5 File does not have pixel data in expected format. Expected a dataset with name="+h5Convertor.H5_DATASET_NAME)

if __name__ == '__main__':
    main()
