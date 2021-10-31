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
5 minutes on the **Raspberry Pi**.

### Preparation / pre processing
Pre processing took the form of updating the symbol set to best fit the data. We took this approach because refining the symbol set was the approach taken by the highest scoring submissions in Project 1. Piazza was extremely helpful for this as it allowed the class to collaborate and add/remove characters since the set was quite different to project 1. We made some changes to the list on Piazza to best fit our data, including removing some characters that may have been valid but did not come up enough in our data to justify their similarity with other characters which may confuse the Model
#### Timing:
N/A

### Training set creation
The image generation code was adapted from that of the first assignment code. Some argumnts were changed to constants to make it easier to use for the user, such as the width, height, symbols file and captcha length, as these were constants for this particular problem. Each captcha was of variable length rather than fixed length, between 1 and 6. Some characters in the symbol set were unsuitable for file names, so these were substituted for suitable characters not in the symbol set. The training script would later read the filenames and make the substitutions back before training. We chose to train with 500k images.
#### Timing:
1.5 hours on **personal machine**.

### Validation set creation
The validation images were created using the same code as the training images. We chose to use 25k images for validation.
#### Timing:
5 Minutes on **personal machine**.

### Model Training
The Training script was also adapted from that used for the first assignment. The conversion to a TFLite model was added to the end of the script, so the output would automatically be ready to run on the pi. When reading the traning data, files with less than six characters were padded with an extra symbol so that they would all be of the same length. This allows the same model to process captchas of any length (Up to 6). We used a batch size of 32, and ran over 5 epochs.
#### Timing
2.5 Hours on **Personal Machine**.

### Classification
The image classification remained unchanged from the first assignment, as the changes were captured in the model passed to the classification script. The script uses a TensorFlow Lite interpreter on the model. It loads each image in the image directory using OpenCV, and puts it through the interpreter. Each result is written to the CSV output file. The padding characters are ignored in the output, so the result is of the correct length. 
#### Timing:
5 minutes on the **Raspberry Pi**.