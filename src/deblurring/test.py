import model, loss, utils
import os
import argparse
import numpy as np


def test(xTest, gtTest, modelPath):
    generator = model.generatorModel()
    generator.load_weights(modelPath)
    x = np.zeros((1,)+xTest.shape)
    print("Shape of batch array " + str(x.shape))
    print("Shape of xTest " + str(xTest.shape))
    x[0,:,:,:,:] = xTest
    predictedOutput = generator.predict(x = x, batch_size=1)
    predictedOutput = predictedOutput[0]
    return  predictedOutput, loss.l1Error(gtTest, predictedOutput)


def main():
    parser = argparse.ArgumentParser(description='DeBlurr knee image data')
    parser.add_argument('-xTest', '--xTest-dicom-dir', help='path to Blurred test data DICOM directory')
    parser.add_argument('-gtTest', '--gtTest-dicom-dir', help='path to Sharp test data DICOM directory')
    parser.add_argument('-model', '--model', help='path to model directory')
    args = parser.parse_args()

    if(not (os.path.exists(args.xTest_dicom_dir) and os.path.exists(args.gtTest_dicom_dir) and os.path.exists(args.model)) ):
        print("Some input path does not exist")
        exit(1)

    print("Create output path.")
    testDir = args.xTest_dicom_dir[:args.xTest_dicom_dir[:-1].rfind("/")]
    outputDir = os.path.join(testDir, "prediction")
    if(not os.path.exists(outputDir)):
        os.mkdir(outputDir)
    print("Output Path created at {}".format(outputDir))

    print("Start loading test data...")
    xTest, gtTest = utils.loadDataDict(args.xTest_dicom_dir, args.gtTest_dicom_dir)
    print("Finished loading data.")

    print("Processing test data...")
    for case,x in xTest.items():
        x = utils.preProcessSingle(x)
        y = utils.preProcessSingle(gtTest[case])
        predictedOutput, predictionLoss = test(x,y,args.model)
        print("Shape of predictedOutput before deprocessing "+ str(predictedOutput.shape))
        predictedOutput = utils.deProcessSingle(predictedOutput)
        with open('L1Loss.txt', 'a') as f:
            f.write('{} - {}\n'.format(case, predictionLoss))
        pDir = "P"+case[case.index("case")+len("case"):]+"_dcm"
        caseDicomDir = os.path.join(case,pDir)
        utils.write3DVolumeToDicom(os.path.join(args.xTest_dicom_dir,caseDicomDir),predictedOutput,os.path.join(outputDir,caseDicomDir))

if __name__ == '__main__':
    main()
