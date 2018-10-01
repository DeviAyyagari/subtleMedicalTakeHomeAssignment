from keras.layers import Input, Conv2D, Conv2DTranspose, Activation, BatchNormalization
from keras.layers.merge import Add
from keras.layers.core import Dropout

imageShape = (512, 512, 252)
numResBlocks = 3

def residualBlock(input, filters, kernel_size=(3, 3), strides=(1, 1)):

    x = Conv2D(filters = filters, kernel_size = kernel_size, strides = strides, padding = valid)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Dropout(0.5)(x)

    x = Conv2D(filters = filters, kernel_size = kernel_size, strides = strides, padding = valid)(x)
    x = BatchNormalization()(x)

    merged = Add()([input, x])
    return merged

def generatorModel():
    inputs = Input(shape = imageShape)

    x = Conv2D(filters = 64, kernel_size=(7, 7), padding='valid')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    x = Conv2D(filters = 128, kernel_size=(3, 3), strides = 2, padding='same')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    x = Conv2D(filters = 256, kernel_size=(3, 3), strides = 2, padding='same')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    for i in range(numResBlocks):
        x = res_block(x, 256)

    x = Conv2DTranspose(filters = 128, kernel_size=(3, 3), strides = 2, padding='same')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    x = Conv2DTranspose(filters = 64, kernel_size=(3, 3), strides = 2, padding='same')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    x = Conv2D(filters = 252, kernel_size=(7, 7), padding='valid')(x)
    x = Activation('tanh')(x)

    outputs = Add()([x, inputs])
    outputs = Lambda(lambda z: z/2)(outputs)

    model = Model(inputs = inputs, outputs = outputs, name = 'Generator')
    return model

def discriminatorModel():
    inputs = Input(shape = imageShape)

    x = Conv2D(filters = 64, kernel_size = (4, 4), strides = 2, padding = 'same')(inputs)
    x = LeakyReLU(0.2)(x)

    x = Conv2D(filters = 64, kernel_size = (4, 4), strides = 2, padding = 'same')(x)
    x = BatchNormalization()(x)
    x = LeakyReLU(0.2)(x)

    x = Conv2D(filters = 128, kernel_size = (4, 4), strides = 2, padding = 'same')(x)
    x = BatchNormalization()(x)
    x = LeakyReLU(0.2)(x)

    x = Conv2D(filters = 256, kernel_size = (4, 4), strides = 2, padding = 'same')(x)
    x = BatchNormalization()(x)
    x = LeakyReLU(0.2)(x)

    x = Conv2D(filters = 512, kernel_size = (4, 4), strides = 1, padding = 'same')(x)
    x = BatchNormalization()(x)
    x = LeakyReLU(0.2)(x)

    x = Conv2D(filters = 1, kernel_size = (4, 4), strides = 1, padding = 'same')(x)

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
