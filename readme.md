# Scalable Project 2
## Usage
### Get Files:
Retrieves the image files for the specified username and places them in a username_images repository.
Eg. `python getFiles.py --username username`

### Generate:
Generates captchas for use in training
Eg. `python generate.py --count 250000 --output-dir train`

### Train: 
Trains a model and outputs it as a tflite file.
Eg. `python train.py --train-dataset train --validate-dataset test --output-model-name model --epochs 5`

### Classify
Uses a tensorflow-lite model to classify captchas. 
Eg. `python classify.py --model-name model --captcha-dir username_images --output username_model.csv --symbols symbols.txt --username username`
 
## Symbol substitution:
- An extra symbol is used in the ML model to represent padding to 6 characters, represented by an index equal to the lenght of the symbol list
- Some symbols don't work in filenames, and are substituted thusly:
- ':' -> 'a'
- '\' -> 'b'
- '|' -> 'd' # Removed, '|' does not appear to be present in the captcha set.

## Summary Details
### File retrieval
Lorem ipsum
#### Timing:
Lorem ipsum.

### Preparation / pre processing
Lorem ipsum
#### Timing:
Lorem ipsum.

### Training set creation
Lorem ipsum
#### Timing:
Lorem ipsum.

### Validation set creation
Lorem ipsum
#### Timing:
Lorem ipsum.

### Solution file generation
Lorem ipsum
#### Timing:
Lorem ipsum.