import os
import re
from . import h5Convertor

def allDicomOps(inputDir, op, **payload):
    """
    Assume a directory structure like
    inputDir/
        - case1
            -- case1_dcm
            -- case1_hdf5
            ...
            -- case1_***
        - case2
            -- case2_dcm
            -- case2_hdf5
            ...
            -- case2_***
        ...
        - caseN
            -- caseN_dcm
            -- caseN_hdf5
            ...
            -- caseN_***
    inputDir/<case_i>/<***_dcm>/*.dcm
    Assume <***_dcm> matches regular expression ".*?_dcm$"

    Performs op on each individual dataset by calling op(<***_dcm>)

    Returns: a dict with key=<case_i> and values=op(<***_dcm>)
    """
    result = {}
    cases = (dir for dir in os.listdir(inputDir) if os.path.isdir(os.path.join(inputDir, dir)))
    dcm_dir_re = ".*?_dcm$"
    dcm_dir_pattern = re.compile(dcm_dir_re)
    for case in cases:
        casePath = os.path.join(inputDir, case)
        dcm_dir = None
        for subDir in os.listdir(casePath):
            if(dcm_dir_pattern.match(subDir)):
                dcm_dir = subDir
                break
        if(not dcm_dir):
            print("No Directory in {0} matches regular exp {1}. Ignore directory".format(casePath, dcm_dir_re))
            continue
        result[case] = op(os.path.join(casePath, dcm_dir), caseName=case, dcmDirName=dcm_dir, **payload)

    return result

def allDicomTo3DVolumes(inputDir):
    """
    Return: a dict with key=<case_i> and values=3DVolume of all dcm files under <***_dcm>
    """
    volumes3D = allDicomOps(inputDir, h5Convertor.dicomTo3DVolume)
    volumes = list()
    for case in sorted(volumes3D.keys()):
        volumes.append(volume3D[case])
    return volumes
