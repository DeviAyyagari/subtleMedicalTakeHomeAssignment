import sys
sys.path.append("../../src")
from dicomUtils import h5Convertor
from scipy.ndimage import gaussian_filter
import argparse
import os

def blurring3d(array3D, sigma):
    return gaussian_filter(array3D, sigma)

def main():
    parser = argparse.ArgumentParser(description='Apply guassian blur filter on dicom files')
    parser.add_argument('--i', '--input-dicom', help='path to input DICOM directory')
    parser.add_argument('--o', '--output-dicom', help='path to output DICOM directory. If the path does not exist, specified path is created')

    args = parser.parse_args()

    if(not os.path.exists(args.o)):
        os.mkdirs(args.o)

    array3D = h5Convertor.dicomTo3DVolume(args.i)
    blurredVolume = blurring3d(array3D, 5)
    h5Convertor.volume3DToDicom(args.i, blurredVolume, args.o)

if __name__ == '__main__':
    main()
