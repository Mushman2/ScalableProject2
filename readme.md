# Scalable Project 2
## Usage
### Generate:
Generates captchas for use in training
Eg. > python generate.py --count 500000 --output-dir train

Timing: Around 1.5 hours, 500K images, was running in background most of the time

### Train: 
Trains a model and outputs it as a tflite file.
Eg. > python train.py --train-dataset train --validate-dataset test --output-model-name model --epochs 5

Timing: GPU training, batch size 32, 500K training data points, 5 epochs. ~2.5 Hours. 

### Classify
Uses a tensorflow-lite model to classify captchas. 
Eg. > python classify.py --model-name model --captcha-dir username_images --output username_model.csv --symbols symbols.txt --username username


## Symbol substitution:
- An extra symbol is used in the ML model to represent padding to 6 characters, represented by an index equal to the lenght of the symbol list
- Some symbols don't work in filenames, and are substituted thusly:
- ':' -> 'a'
- '\' -> 'b'
- '|' -> 'd' # Removed, '|' does not appear to be present in the captcha set.