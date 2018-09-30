import argparse
import h5Convertor

def main():
    parser = argparse.ArgumentParser(description='Covert dicom files to hdf5 format')
    parser.add_argument('--i', '--input-dicom', help='path to input DICOM directory')
    parser.add_argument('--h', '--output-hdf5', help='path to output hdf5 file')

    args = parser.parse_args()

    if(args.h.split(".")[-1] != "hdf5"):
        args.h += ".hdf5"

    h5Convertor.dicomToH5(args.i, args.h)

if __name__ == '__main__':
    main()
