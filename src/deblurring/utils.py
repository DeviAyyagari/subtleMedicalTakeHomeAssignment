import sys
sys.path.append("../../src")

from dicomUtils.dicomOps import allDicomTo3DVolumes

def loadData(xDicomPath, gtDicomPath):
    xTrain = allDicomTo3DVolumes(xDicomPath)
    gtTrain = allDicomTo3DVolumes(gtDicomPath)

    return xTrain, gtTrain

def preProcessData(xData, gtData):
    for index in range(len(xData)):
        xData[index] = (xData[index] - 127.5) / 127.5
        gtData[index] = (gtData[index] - 127.5) / 127.5

    return xData, gtData

def deProcessData(xData, gtData):
    for index in range(len(xData)):
        xData[index] = (xData[index] * 127.5) + 127.5
        gtData[index] = (gtData[index] * 127.5) + 127.5

    return xData, gtData
