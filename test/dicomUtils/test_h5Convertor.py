import sys
sys.path.append("../../src")
from dicomUtils import h5Convertor
import unittest

class TestH5Convertor(unittest.TestCase):
    def test_readFilesInDir(self):
        dirPath = "../testData/good_data/case1/P1_dcm"
        expectedFileNames = ['Sec_250.mag', 'Sec_251.mag']
        fileNames = h5Convertor.readFilesInDir(dirPath)
        for i,f in enumerate(sorted(fileNames)): self.assertEqual(f, expectedFileNames[i])

    def test_readCaseData(self):
        dirPath = "../testData/good_data"
        expectedDataDict = {"P1_dcm":['Sec_250.mag', 'Sec_251.mag'], "P2_dcm":['Sec_250.mag', 'Sec_251.mag']}
        data = h5Convertor.readCaseData(dirPath)
        self.assertEqual(data, expectedDataDict)

    def test_readCaseDataBad(self):
        dirPath = "../testData/bad_data"
        expectedDataDict = {}
        data = h5Convertor.readCaseData(dirPath)
        self.assertEqual(data, expectedDataDict)

if __name__ == '__main__':
    unittest.main()
