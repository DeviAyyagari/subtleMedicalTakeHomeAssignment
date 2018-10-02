import sys
sys.path.append("../../src")

from dicomUtils.dicomOps import allDicomTo3DVolumes, allDicomOps
from dicomUtils import h5Convertor
import os

def loadData(xDicomPath, gtDicomPath):
    x = allDicomTo3DVolumes(xDicomPath)
    gt = allDicomTo3DVolumes(gtDicomPath)

    return x, gt

def loadDataDict(xDicomPath, gtDicomPath):
    x = allDicomOps(xDicomPath, h5Convertor.dicomTo3DVolumeReshaped)
    gt = allDicomOps(gtDicomPath, h5Convertor.dicomTo3DVolumeReshaped)

    return x, gt

def write3DVolumeToDicom(dicomInputPath, array3D, outputDicomDir):
    if(not os.path.exists(outputDicomDir)):
        os.makedirs(outputDicomDir)
    array3D = array3D.reshape(array3D.shape[0],array3D.shape[1], array3D.shape[3])
    h5Convertor.volume3DToDicom(dicomInputPath, array3D, outputDicomDir)

def preProcessSingle(data):
    data = (data - 127.5) / 127.5
    return data

def preProcessData(xData, gtData):
    for index in range(xData.shape[0]):
        #xData[index] = xData[index].reshape((512,512,1,252))
        #gtData[index] = gtData[index].reshape((512,512,1,252))
        xData[index] = preProcessSingle(xData[index])
        gtData[index] = preProcessSingle(gtData[index])

    return xData, gtData

def deProcessSingle(data):
    data = (data * 127.5) + 127.5
    return data

def deProcessData(xData, gtData):
    for index in range(len(xData)):
        xData[index] = deProcessSingle(xData[index])
        gtData[index] = deProcessSingle(gtData[index])

    return xData, gtData
