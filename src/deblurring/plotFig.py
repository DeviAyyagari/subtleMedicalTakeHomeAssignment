import matplotlib.pyplot as plt
import sys
sys.path.append("../../src")
from dicomUtils import h5Convertor
import argparse


parser = argparse.ArgumentParser(description='DeBlurr knee image data')
parser.add_argument('-dicom', '--dicom', help='path to DICOM directory')

args = parser.parse_args()

dicom = h5Convertor.dicomTo3DVolume(args.dicom)
imgplot = plt.imshow(dicom[:,:,125], cmap='gray')
plt.show()
