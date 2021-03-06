#!/usr/bin/env python3

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import cv2
import numpy
import string
import random
import argparse
import tensorflow as tf
import tensorflow.keras as keras
import datetime

def create_model(captcha_length, captcha_num_symbols, input_shape, model_depth=5, module_size=2):
  input_tensor = keras.Input(input_shape)
  x = input_tensor
  for i, module_length in enumerate([module_size] * model_depth):
      for j in range(module_length):
          x = keras.layers.Conv2D(32*2**min(i, 3), kernel_size=3, padding='same', kernel_initializer='he_uniform')(x)
          x = keras.layers.BatchNormalization()(x)
          x = keras.layers.Activation('relu')(x)
      x = keras.layers.MaxPooling2D(2)(x)

  x = keras.layers.Flatten()(x)
  x = [keras.layers.Dense(captcha_num_symbols, activation='softmax', name='char_%d'%(i+1))(x) for i in range(captcha_length)]
  model = keras.Model(inputs=input_tensor, outputs=x)

  return model

class ImageSequence(keras.utils.Sequence):
    def __init__(self, directory_name, batch_size, captcha_length, captcha_symbols, captcha_width, captcha_height):
        self.directory_name = directory_name
        self.batch_size = batch_size
        self.captcha_length = captcha_length
        self.captcha_symbols = captcha_symbols
        self.captcha_width = captcha_width
        self.captcha_height = captcha_height

        file_list = os.listdir(self.directory_name)
        random.shuffle(file_list)
        self.files = dict(zip(map(lambda x: x.split('.')[0], file_list), file_list))
        self.key_list = list(self.files.keys())
        

        self.count = len(file_list)

    def __len__(self):
        return int(numpy.floor(self.count / self.batch_size))

    def __getitem__(self, idx):
        X = numpy.zeros((self.batch_size, self.captcha_height, self.captcha_width, 3), dtype=numpy.float32)
        y = [numpy.zeros((self.batch_size, len(self.captcha_symbols)+1), dtype=numpy.uint8) for i in range(self.captcha_length)]

        for i in range(self.batch_size):

            image_label = self.key_list[idx*self.batch_size+i]
            image_file = self.files[image_label]

            raw_data = cv2.imread(os.path.join(self.directory_name, image_file))
            rgb_data = cv2.cvtColor(raw_data, cv2.COLOR_BGR2RGB)
            processed_data = numpy.array(rgb_data) / 255.0
            X[i] = processed_data

            image_label = image_label.split('_')[0]
            while len(image_label) < 6:
                image_label = image_label + " "

            for j, ch in enumerate(image_label):
                y[j][i, :] = 0
                if ch == "a": ch = ':'
                if ch == "b": ch = '\\'
                if ch == " ":
                    y[j][i, len(self.captcha_symbols)] = 1
                else:
                    y[j][i, self.captcha_symbols.find(ch)] = 1

        return X, y

def main():
    parser = argparse.ArgumentParser()
    captchaWidth = 128
    captchaHeight = 64
    captchaMinLength = 1
    captchaMaxLength = 6
    symbolsDir = "symbols.txt"
    batchSize = 32

    parser.add_argument('--train-dataset', help='Where to look for the training image dataset', type=str)
    parser.add_argument('--validate-dataset', help='Where to look for the validation image dataset', type=str)
    parser.add_argument('--output-model-name', help='Where to save the trained model', type=str)
    parser.add_argument('--input-model', help='Where to look for the input model to continue training', type=str)
    parser.add_argument('--epochs', help='How many training epochs to run', type=int)
    args = parser.parse_args()

    if args.epochs is None:
        print("Please specify the number of training epochs to run")
        exit(1)

    if args.train_dataset is None:
        print("Please specify the path to the training data set")
        exit(1)

    if args.validate_dataset is None:
        print("Please specify the path to the validation data set")
        exit(1)

    if args.output_model_name is None:
        print("Please specify a name for the trained model")
        exit(1)

    captcha_symbols = None
    with open(symbolsDir) as symbols_file:
        captcha_symbols = symbols_file.readline()

    with tf.device('/device:GPU:0'):
        model = create_model(captchaMaxLength, len(captcha_symbols) + 1, (captchaHeight, captchaWidth, 3))

        if args.input_model is not None:
            model.load_weights(args.input_model)

        model.compile(loss='categorical_crossentropy',
                      optimizer=keras.optimizers.Adam(1e-3, amsgrad=True),
                      metrics=['accuracy'])

        model.summary()

        training_data = ImageSequence(args.train_dataset, batchSize, captchaMaxLength, captcha_symbols, captchaWidth, captchaHeight)
        validation_data = ImageSequence(args.validate_dataset, batchSize, captchaMaxLength, captcha_symbols, captchaWidth, captchaHeight)

        callbacks = [keras.callbacks.ModelCheckpoint(args.output_model_name+'.h5', save_best_only=False)]

        with open(args.output_model_name+".json", "w") as json_file:
            json_file.write(model.to_json())

        try:
            model.fit(x=training_data,
                                validation_data=validation_data,
                                epochs=args.epochs,
                                callbacks=callbacks,
                                use_multiprocessing=True)
        except KeyboardInterrupt:
            print('KeyboardInterrupt caught, saving current weights as ' + args.output_model_name+'_resume.h5')
            model.save_weights(args.output_model_name+'_resume.h5')

        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        tflite_model = converter.convert()

        with open(args.output_model_name+'.tflite', 'wb') as f:
            f.write(tflite_model)

if __name__ == '__main__':
    begin_time = datetime.datetime.now()
    main()
    print(datetime.datetime.now() - begin_time)