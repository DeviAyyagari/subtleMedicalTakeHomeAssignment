
def readCaseData(dataPath):
    """
    This function reads a directory structure like
    dataPath/case(i)/P(i)_dcm
    and returns the a dict with P(i)_dcm as keys
    and list of dicom filenames as the values
    """

    data = {}
    cases = (dir for dir in listdir(dataPath) if isdir(join(dataPath, dir)))
    for case in cases:
        try:
            pDir = listdir(dataPath+"/"+case)[0]
            data[pDir] = readFilesInDir(dataPath + "/" + case + "/" + pDir)
        except Exception as e:
            print(e)
    return data
