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
import tflite_runtime.interpreter as tflite

def decode(characters, y):
    if numpy.argmax(y) == characters.len(): return ""
    return characters[numpy.argmax(y)]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-name', help='Model name to use for classification', type=str)
    parser.add_argument('--captcha-dir', help='Where to read the captchas to break', type=str)
    parser.add_argument('--output', help='File where the classifications should be saved', type=str)
    parser.add_argument('--symbols', help='File with the symbols to use in captchas', type=str)
    parser.add_argument('--username', help='TCD Username', type=str)
    args = parser.parse_args()

    if args.model_name is None:
        print("Please specify the CNN model to use")
        exit(1)

    if args.captcha_dir is None:
        print("Please specify the directory with captchas to break")
        exit(1)

    if args.output is None:
        print("Please specify the path to the output file")
        exit(1)

    if args.symbols is None:
        print("Please specify the captcha symbols file")
        exit(1)

    if args.username is None:
        print("Please specify your TCD Username")
        exit(1)

    symbols_file = open(args.symbols, 'r')
    captcha_symbols = symbols_file.readline().strip()
    symbols_file.close()

    print("Classifying captchas with symbol set {" + captcha_symbols + "}")


    with open(args.output, 'w') as output_file:
        interpreter = tflite.Interpreter(args.model_name)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        output_file.write(args.username + '\n')
        for x in sorted (os.listdir(args.captcha_dir)):
            # load image and preprocess it
            raw_data = cv2.imread(os.path.join(args.captcha_dir, x))
            rgb_data = cv2.cvtColor(raw_data, cv2.COLOR_BGR2RGB)
            image = (numpy.array(rgb_data) / 255.0).astype(numpy.float32)
            (c, h, w) = image.shape
            image = image.reshape([-1, c, h, w])
            interpreter.set_tensor(input_details[0]['index'], image)
            interpreter.invoke()
            print('\nClassified ' + x + ',')
            output_file.write(x + ",")
            for i in range(5):
                #print(decode(captcha_symbols, interpreter.get_tensor(output_details[i]['index'])))
                output_file.write(decode(captcha_symbols, interpreter.get_tensor(output_details[i]['index'])))
            output_file.write('\n')
            #print('Classified ' + x + ',' + decode(captcha_symbols, prediction))

if __name__ == '__main__':
    main()
