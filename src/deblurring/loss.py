import keras.backend as K
from keras.applications.vgg16 import VGG16
from keras.models import Model
import numpy as np

imageShape = (512, 512, 1, 252)

def l1Loss(y_true, y_pred):
    return K.mean(K.abs(y_pred - y_true))

def perceptualLoss(yTrue, yPred):
    vgg = VGG16(include_top = False, weights = 'imagenet', input_shape = imageShape)
    lossModel = Model(inputs = vgg.input, outputs = vgg.get_layer('block3_conv3').output)
    lossModel.trainable = False
    return K.mean(K.square(lossModel(yTrue) - lossModel(yPred)))

def wassersteinLoss(yTrue, yPred):
    return K.mean(yTrue * yPred)
