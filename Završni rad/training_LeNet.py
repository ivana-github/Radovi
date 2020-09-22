import matplotlib

from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.utils import to_categorical
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import img_to_array

import random
from imutils import paths
import numpy as np
import cv2
import os

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from IPython import get_ipython

from klasifikator_maskica import LeNet

# initialize the number of epochs to train for, initial learning rate and batch size
EPOCHS = 150  #optimal number of epochs for classification
INIT_LR = 0.001
BS = 32 #CHANGE

data = []
labels = []

matplotlib.use("Agg")
ipy = get_ipython()
base_dir = "slike"

# Dictionary containting path to dataset in mounted google drive
args = {
 "dataset": base_dir ,
 "model": "model.h5",
 "plot" :"plot.png"
}

print("[INFO] loading images...")
# grab the image paths and randomly shuffle them
imagePaths = sorted(list(paths.list_images(args["dataset"])))
random.seed(42)
random.shuffle(imagePaths)
# loop over the input images
for imagePath in imagePaths:
	# load the image, pre-process it, and store it in the data list
	image = cv2.imread(imagePath)
	image = cv2.resize(image, (64,64))
	image = img_to_array(image)
	data.append(image)
	# extract the class label from the image path and update the labels list
	label = imagePath.split(os.path.sep)[-2]
	label = 1 if label == "no-mask" else 0
	labels.append(label)

# scale the raw pixel intensities to the range [0, 1]
print("done with imagePaths")
data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)

lb = LabelBinarizer().fit(labels)
labels = lb.transform(labels)
labels = to_categorical(labels)

# partition the data into training and testing splits using 75% of
# the data for training and the remaining 25% for testing
(trainX, testX_1, trainY, testY_1) = train_test_split(data,
	labels, test_size=0.30, random_state=42)

# convert the labels from integers to vectors
x_test = testX_1[:-round(len(testX_1)/2)]
y_test = testY_1[:-round(len(testX_1)/2)]
testY = testY_1[-round(len(testX_1)/2):]
testX = testX_1[-round(len(testX_1)/2):]

# construct the image generator for data augmentation
aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
	height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
	horizontal_flip=True, fill_mode="nearest")

# initialize the model
print("[INFO] compiling model...")
model = LeNet.build(width=64, height=64, depth=3, classes=2)
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)

model.compile(loss="binary_crossentropy", optimizer=opt,
	metrics=["accuracy"])

# train the network
print("[INFO] training network...")
H = model.fit_generator(aug.flow(trainX, trainY, batch_size=BS),steps_per_epoch=len(trainX) // BS,
    validation_data=(testX, testY), epochs=EPOCHS, verbose=1)


# make predictions on the testing set
print("[INFO] evaluating network...")
results = model.evaluate(x_test, y_test, batch_size=BS)
print('test loss, test acc:', results, '\n')


if ipy is not None:
    ipy.run_line_magic('matplotlib', 'inline')

img = mpimg.imread('plot.png')
imgplot = plt.imshow(img)

