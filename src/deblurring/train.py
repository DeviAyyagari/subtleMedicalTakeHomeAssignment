import os
import model, loss, utils
import argparse
import numpy as np
from keras.optimizers import Adam


def saveWeights(discriminator, generator, epoch, loss):
    saveDir = "model/"
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
    generator.save_weights(os.path.join(saveDir, 'generator.h5'), True)
    discriminator.save_weights(os.path.join(saveDir, 'discriminator.h5'), True)

def learn(xTrain, gtTrain, batchSize = 3, epochs = 250, discriminatorUpdates = 5):
    print("Start learning on training set.")
    generator = model.generatorModel()
    discriminator = model.discriminatorModel()
    discOnGen = model.generatorContainingDiscriminator(generator, discriminator)

    discOptimizer = Adam(lr = 1E-4, beta_1 = 0.9, beta_2 = 0.999, epsilon = 1e-08)
    discOnGenOptimizer = Adam(lr = 1E-4, beta_1 = 0.9, beta_2 = 0.999, epsilon = 1e-08)

    discriminator.trainable = True
    discriminator.compile(optimizer = discOptimizer, loss = loss.wassersteinLoss)
    discriminator.trainable = False
    lossModel = [loss.l1Loss, loss.wassersteinLoss]
    loss_weights = [100, 1]
    discOnGen.compile(optimizer = discOnGenOptimizer, loss = lossModel, loss_weights = loss_weights)
    discriminator.trainable = True

    outputTrueBatch, outputFalseBatch = np.ones((batchSize, 1)), -np.ones((batchSize, 1))

    for epoch in range(epochs):
        print('epoch: {}/{}'.format(epoch, epochs))
        print('batches: {}'.format(xTrain.shape[0] / batchSize))

        permutatedIndexes = np.random.permutation(xTrain.shape[0])

        discLosses = []
        discOnGenLosses = []
        for index in range(xTrain.shape[0] // batchSize):
            batchIndeces = permutatedIndexes[index*batchSize:(index+1)*batchSize]
            xTrainBatch = xTrain[batchIndeces]
            gtTrainBatch = gtTrain[batchIndeces]

            fakeImages = generator.predict(x=xTrainBatch, batch_size=batchSize)

            for _ in range(discriminatorUpdates):
                lossReal = discriminator.train_on_batch(gtTrainBatch, outputTrueBatch)
                lossFake = discriminator.train_on_batch(fakeImages, outputFalseBatch)
                discLoss = 0.5 * np.add(lossReal, lossFake)
                discLosses.append(discLoss)
            print('batch {} discriminator loss : {}'.format(index+1, np.mean(discLosses)))

            discriminator.trainable = False

            disOnGenLoss = discOnGen.train_on_batch(xTrainBatch, [gtTrainBatch, outputTrueBatch])
            discOnGenLosses.append(disOnGenLoss)
            print('batch {} disc on gen loss : {}'.format(index+1, disOnGenLoss))

            discriminator.trainable = True

        with open('log.txt', 'a') as f:
            f.write('{} - {} - {}\n'.format(epoch, np.mean(discLosses), np.mean(discOnGenLosses)))

        saveWeights(discriminator, generator, epoch, int(np.mean(discOnGenLosses)))

def main():
    parser = argparse.ArgumentParser(description='DeBlurr knee image data')
    parser.add_argument('-xTrain', '--xTrain-dicom-dir', help='path to Blurred training data DICOM directory')
    parser.add_argument('-gtTrain', '--gtTrain-dicom-dir', help='path to Sharp training data DICOM directory')
    args = parser.parse_args()

    if(not (os.path.exists(args.xTrain_dicom_dir) and os.path.exists(args.gtTrain_dicom_dir))):
        print("Some input path does not exist")
        exit(1)

    print("Start loading training data...")
    xTrain, gtTrain = utils.loadData(args.xTrain_dicom_dir, args.gtTrain_dicom_dir)
    print("Finished loading data.")
    xTrain, gtTrain = utils.preProcessData(xTrain, gtTrain)
    print("Finished preprocessing data.")
    learn(xTrain, gtTrain)

if __name__ == '__main__':
    main()
