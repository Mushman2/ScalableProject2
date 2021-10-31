# Scalable Project 2
## Usage

### Get Files:
Retrieves the image files for the specified username and places them in a `username_images` repository.

`python getFiles.py --username username`

### Generate:
Generates captchas for use in training
`python generate.py --count 250000 --output-dir train`



### Train: 
Trains a model and outputs it as a tflite file.
`python train.py --train-dataset train --validate-dataset test --output-model-name model --epochs 5`



### Classify
Uses a tensorflow-lite model to classify captchas. 
`python classify.py --model-name model --captcha-dir username_images --output username_model.csv --symbols symbols.txt --username username`


## Symbol substitution:
- An extra symbol is used in the ML model to represent padding to 6 characters, represented by an index equal to the lenght of the symbol list
- Some symbols don't work in filenames, and are substituted thusly:
- ':' -> 'a'
- '\' -> 'b'

## Summary Details
### File retrieval
The file retrieval is a four-step process. 
1. The script contacts the image server with the shortname of the user. This returns a HTML page containing a link element to the CSV of image names. 
2. The script parses the link out and fetches this CSV. 
3. The script iterates through the CSV and contacts the image server with each filename and the shortname. Each response is a HTML page containing a link element to the image. 
4. The script parses out each link and saves each image response. 

#### Timing:
Lorem ipsum.

### Preparation / pre processing
Lorem ipsum
#### Timing:
Lorem ipsum.

### Training set creation
Lorem ipsum
#### Timing:
Around 1.5 hours, 500K images

### Validation set creation
Lorem ipsum
#### Timing:
Around 5 Mins, 25K images

### Model Training

#### Timing
GPU training, batch size 32, 500K training data points, 5 epochs. ~2.5 Hours. 

### Solution file generation
Lorem ipsum
#### Timing:
Lorem ipsum.