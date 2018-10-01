import sys
sys.path.append("../../src")
from dicomUtils import h5Convertor, dicomOps
from scipy.ndimage import gaussian_filter
import argparse
import os

def blurring3d(array3D, sigma):
    return gaussian_filter(array3D, sigma)

def makeFilteredCase(inputDicomPath, outputDicomPath, sigma, caseName=None, dcmDirName=None):
    if(caseName):
        outputDicomPath = os.path.join(outputDicomPath, caseName)
        if(dcmDirName):
            outputDicomPath = os.path.join(outputDicomPath, dcmDirName)

    if(os.path.exists(outputDicomPath)):
        print("{} already exists. Skip applying Gaussian blur filter to this case.".format(outputDicomPath))
        return
    else:
        os.makedirs(outputDicomPath)

    print("Creating Guassian Blur Filtered images from {} to {}".format(inputDicomPath, outputDicomPath))

    array3D = h5Convertor.dicomTo3DVolume(inputDicomPath)
    blurredVolume = blurring3d(array3D, sigma)
    h5Convertor.volume3DToDicom(inputDicomPath, blurredVolume, outputDicomPath)

def makeFilteredDataset(inputDicomPath, outputDicomPath, sigma):
    print("Creating Guassian Blur Filtered images for all cases under {} to {}".format(inputDicomPath, outputDicomPath))
    dicomOps.allDicomOps(inputDicomPath, makeFilteredCase, outputDicomPath=outputDicomPath, sigma=sigma)

def main():
    parser = argparse.ArgumentParser(description='Apply guassian blur filter on dicom files')
    parser.add_argument('--i', '--input-dicom', help='path to input DICOM directory')
    parser.add_argument('--o', '--output-dicom', help='path to output DICOM directory. If the path does not exist, specified path is created')

    args = parser.parse_args()

    if(not os.path.exists(args.i)):
        print("Input Dicom Path does not exist. Exit")
        exit(1)

    sigma = 5
    makeFilteredCase(args.i, args.o, sigma)

if __name__ == '__main__':
    main()
