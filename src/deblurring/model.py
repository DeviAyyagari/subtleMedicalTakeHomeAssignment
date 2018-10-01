from keras.layers import Input, Conv3D, Conv3DTranspose, Activation, BatchNormalization
from keras.layers.merge import Add
from keras.layers.core import Dropout
from keras.layers.core import Dense, Flatten, Lambda
from keras.models import Model
from keras.layers.advanced_activations import LeakyReLU


imageShape = (512, 512, 1, 252)
numResBlocks = 3

def residualBlock(input, filters, kernel_size=(3, 3, 1), strides=(1, 1, 1)):

    x = Conv3D(filters = filters, kernel_size = kernel_size, strides = strides, padding = 'same')(input)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Dropout(0.5)(x)

    x = Conv3D(filters = filters, kernel_size = kernel_size, strides = strides, padding = 'same')(x)
    x = BatchNormalization()(x)

    merged = Add()([input, x])
    return merged

def generatorModel():
    inputs = Input(shape = imageShape)

    x = Conv3D(filters = 64, kernel_size=(7, 7, 1), padding='same')(inputs)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    x = Conv3D(filters = 128, kernel_size=(3, 3, 1), strides = (2,2,1), padding='same')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    x = Conv3D(filters = 256, kernel_size=(3, 3, 1), strides = (2,2,1), padding='same')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    for i in range(numResBlocks):
        x = residualBlock(x, 256)

    x = Conv3DTranspose(filters = 128, kernel_size=(3, 3, 1), strides = (2,2,1), padding='same')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    x = Conv3DTranspose(filters = 64, kernel_size=(3, 3, 1), strides = (2,2,1), padding='same')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    x = Conv3D(filters = 252, kernel_size=(7, 7, 1), padding='same')(x)
    x = Activation('tanh')(x)

    outputs = Add()([x, inputs])
    outputs = Lambda(lambda z: z/2)(outputs)

    model = Model(inputs = inputs, outputs = outputs, name = 'Generator')
    return model

def discriminatorModel():
    inputs = Input(shape = imageShape)

    x = Conv3D(filters = 64, kernel_size = (4, 4, 1), strides = (2,2,1), padding = 'same')(inputs)
    x = LeakyReLU(0.2)(x)

    x = Conv3D(filters = 64, kernel_size = (4, 4, 1), strides = (2,2,1), padding = 'same')(x)
    x = BatchNormalization()(x)
    x = LeakyReLU(0.2)(x)

    x = Conv3D(filters = 128, kernel_size = (4, 4, 1), strides = (2,2,1), padding = 'same')(x)
    x = BatchNormalization()(x)
    x = LeakyReLU(0.2)(x)

    x = Conv3D(filters = 256, kernel_size = (4, 4, 1), strides = (2,2,1), padding = 'same')(x)
    x = BatchNormalization()(x)
    x = LeakyReLU(0.2)(x)

    x = Conv3D(filters = 512, kernel_size = (4, 4, 1), strides = 1, padding = 'same')(x)
    x = BatchNormalization()(x)
    x = LeakyReLU(0.2)(x)

    x = Conv3D(filters = 1, kernel_size = (4, 4, 1), strides = 1, padding = 'same')(x)

    x = Flatten()(x)
    x = Dense(1024, activation = 'tanh')(x)
    x = Dense(1, activation = 'sigmoid')(x)

    model = Model(inputs = inputs, outputs = x, name = 'Discriminator')
    return model

def generatorContainingDiscriminator(generator, discriminator):
    inputs = Input(shape = imageShape)
    generated_image = generator(inputs)
    outputs = discriminator(generated_image)
    model = Model(inputs = inputs, outputs = [generated_image, outputs])
    return model
