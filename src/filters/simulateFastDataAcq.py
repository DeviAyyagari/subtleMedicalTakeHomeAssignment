#############################################################
# Simulates fast data acquisition by creating Blurred images
# Takes as input the train and test data paths.
# Expects train and test data paths to have original sharp images under
#    - train
#        -- sharp
#    - test
#        -- sharp
# Simulates fast data acquisition by creating Blurred images under
#   -train
#       -- blurred
#   -test
#       -- blurred
# Passes the paths to deblurring orchestrator to work its magic.
##############################################################

import argparse
import os
import sys

import guassianBlurFilter

def main():
    parser = argparse.ArgumentParser(description='Simulate Fast Data Acquisition and Improve image resolution with Deep learning')
    parser.add_argument('-train', '--train-dicom-dir', default = "./train", help='path to training data DICOM directory')
    parser.add_argument('-test', '--test-dicom-dir', default = "./test", help='path to test data DICOM directory')

    args = parser.parse_args()

    if(not os.path.exists(args.train_dicom_dir)):
        print("Training dir does not exist on path " + args.train_dicom_dir)
        exit(1)
    if(not os.path.exists(args.test_dicom_dir)):
        print("Test dir does not exist on path " + args.test_dicom_dir)
        exit(1)

    #Step 0. Sharp Image paths
    print("Find Sharp images under train and test paths...")

    gtTrainPath = os.path.join(args.train_dicom_dir, "sharp")
    if(not os.path.exists(gtTrainPath)):
        print("Sharp training images don't exists under trainPath/sharp. Abort")
        exit(1)
    gtTestPath = os.path.join(args.test_dicom_dir, "sharp")
    if(not os.path.exists(gtTestPath)):
        print("Sharp test images don't exists under testPath/sharp. Abort")
        exit(1)

    print("Sharp images found under train and test paths.")

    #Step 1. Create xTrain and xTest paths.
    print("Creating blurred image paths...")

    xTrainPath = os.path.join(args.train_dicom_dir, "blurred")
    if(not os.path.exists(xTrainPath)):
        os.mkdir(xTrainPath)

    xTestPath = os.path.join(args.test_dicom_dir, "blurred")
    if(not os.path.exists(xTestPath)):
        os.mkdir(xTestPath)

    print("Created blurred image paths")

    #Step 2. Create blurred images in these paths
    sigma = 5
    print("Creating TRAINING Blurred images from sharp images...")
    guassianBlurFilter.makeFilteredDataset(gtTrainPath, xTrainPath, sigma)
    print("Created TRAINING Blurred images from sharp images.")

    print("Creating TEST Blurred images from sharp images...")
    guassianBlurFilter.makeFilteredDataset(gtTestPath, xTestPath, sigma)
    print("Created TEST Blurred images from sharp images.")

if __name__ == '__main__':
    main()
