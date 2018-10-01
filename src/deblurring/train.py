import os
from . import model, loss, utils
import argparse
import numpy as np
from keras.optimizers import Adam


def saveWeights(discriminator, generator, epoch, loss):
    saveDir = "model/"
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
    g.save_weights(os.path.join(saveDir, 'generator_{}_{}.h5'.format(epoch, loss)), True)
    d.save_weights(os.path.join(saveDir, 'discriminator_{}.h5'.format(epoch)), True)

def learn(xTrain, gtTrain, batchSize = 3, epochs = 100, discriminatorUpdates = 5):

    generator = model.generatorModel()
    discriminator = model.discriminatorModel()
    discOnGen = model.generatorContainingDiscriminator(generator, discriminator)

    discOptimizer = Adam(lr = 1E-4, beta_1 = 0.9, beta_2 = 0.999, epsilon = 1e-08)
    discOnGenOptimizer = Adam(lr = 1E-4, beta_1 = 0.9, beta_2 = 0.999, epsilon = 1e-08)

    discriminator.trainable = True
    discriminator.compile(optimizer = discOptimizer, loss = loss.wassersteinLoss)
    discriminator.trainable = False
    loss = [loss.perceptualLoss, loss.wassersteinLoss]
    loss_weights = [100, 1]
    discOnGen.compile(optimizer = discOnGenOptimizer, loss = loss, loss_weights = loss_weights)
    discriminator.trainable = True

    outputTrueBatch, outputFalseBatch = np.ones((batchSize, 1)), -np.ones((batchSize, 1))

    for epoch in range(epochs):
        print('epoch: {}/{}'.format(epoch, epochs))
        print('batches: {}'.format(len(xTrain) / batchSize))

        permutatedIndexes = np.random.permutation(len(xTrain))

        discLosses = []
        discOnGenLosses = []
        for index in range(len(xTrain) // batchSize):
            batchIndeces = permutatedIndexes[index*batchSize:(index+1)*batchSize]
            xTrainBatch = xTrain[batchIndeces]
            gtTrainBatch = gtTrain[batchIndeces]

            fakeImages = generator.predict(x=xTrainBatch, batch_size=batchSize)

            for _ in range(discriminatorUpdates):
                lossReal = discriminator.train_on_batch(gtTrainBatch, outputTrueBatch)
                lossFake = discriminator.train_on_batch(fakeImages, outputFalseBatch)
                loss = 0.5 * np.add(lossReal, lossFake)
                discLosses.append(loss)
            print('batch {} discriminator loss : {}'.format(index+1, np.mean(discLosses)))

            discriminator.trainable = False

            loss = discOnGen.train_on_batch(xTrainBatch, [gtTrainBatch, outputTrueBatch])
            discOnGenLosses.append(loss)
            print('batch {} disc on gen loss : {}'.format(index+1, loss))

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

    xTrain, gtTrain = utils.loadData(args.xTrain_dicom_dir, args.gtTrain_dicom_dir)
    xTrain, gtTrain = utils.preProcessData(xTrain, gtTrain)
    learn(xTrain, gtTrain)

if __name__ == '__main__':
    main()
