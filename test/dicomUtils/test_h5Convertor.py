import sys
sys.path.append("../../src")
from dicomUtils import h5Convertor
import unittest

class TestH5Convertor(unittest.TestCase):
    def test_readFilesInDir(self):
        dirPath = "../testData/case1/P1_dcm"
        expectedFileNames = ['Sec_250.mag', 'Sec_251.mag']
        fileNames = h5Convertor.readFilesInDir(dirPath)
        for i,f in enumerate(sorted(fileNames)): self.assertEqual(f, expectedFileNames[i])

if __name__ == '__main__':
    unittest.main()
