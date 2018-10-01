import sys
sys.path.append("../../src")

import os
from dicomUtils.dicomOps import allDicomTo3DVolumes
import argparse

def orchestrate(xTrainDicomPath, gtTrainDicomPath, xTestDicomPath, gtTestDicomPath):
    xTrain = allDicomTo3DVolumes(xTrainDicomPath)
    gtTrain = allDicomTo3DVolumes(gtTrainDicomPath)
    xTest = allDicomTo3DVolumes(xTestDicomPath)
    gtTest = allDicomTo3DVolumes(gtTestDicomPath)

def main():
    parser = argparse.ArgumentParser(description='DeBlurr knee image data')
    parser.add_argument('-xTrain', '--xTrain-dicom-dir', help='path to Blurred training data DICOM directory')
    parser.add_argument('-gtTrain', '--gtTrain-dicom-dir', help='path to Sharp training data DICOM directory')
    parser.add_argument('-xTest', '--xTest-dicom-dir', help='path to Blurred test data DICOM directory')
    parser.add_argument('-gtTest', '--gtTest-dicom-dir', help='path to Sharp test data DICOM directory')
    args = parser.parse_args()

    if(not (os.path.exists(args.xTrain_dicom_dir) and
      os.path.exists(args.gtTrain_dicom_dir) and
      os.path.exists(args.xTest_dicom_dir) and
      os.path.exists(args.gtTest_dicom_dir)) ):
        print("Some input path does not exist")
        exit(1)

    orchestrate(args.xTrain_dicom_dir, args.gtTrain_dicom_dir, args.xTest_dicom_dir, args.gtTest_dicom_dir)

if __name__ == '__main__':
    main()
