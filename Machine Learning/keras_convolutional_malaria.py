#Evaluates if image contains a malaria infected or not cell sample. Samples obtained from
#National Library of Medicine. It should be downloaded manually from
#https://drive.google.com/uc?id=1N1gcN8_5dZVlIejoC00QZLSZFhGoSoQb&export=download
#and extracted next to this file.
#TAKES A LOT OF TIME TO TRAIN


import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.image import imread
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import EarlyStopping

#locating data
data_dir = os.path.join(os.path.dirname(__file__),'cell_images')
test_path = data_dir+'\\test\\'
train_path = data_dir+'\\train\\'

#displaing examples of infected and uninfected cells

uninfected_cell_path = train_path+'\\uninfected\\'+os.listdir(train_path+'\\uninfected')[0]
uninfected_cell = imread(uninfected_cell_path)
plt.imshow(uninfected_cell)
plt.show()

infected_cell_path = train_path+'\\parasitized\\'+os.listdir(train_path+'\\parasitized')[0]
infected_cell = imread(infected_cell_path)
plt.imshow(infected_cell)
plt.show()


#Checking an average resolution of our images
height = []
width = []
for image_filename in os.listdir(test_path+'\\uninfected'):
	img = imread(test_path+'\\uninfected'+'\\'+image_filename)
	d1,d2,colors = img.shape
	height.append(d1)
	width.append(d2)

print('Average height: ',np.mean(height))
print('Average width: ',np.mean(width))

#Seems like average picture size is 130*130 so setting this value as standard to reshape all pictures

image_shape = (130,130,3)

#using data generation tool to expand our dataset diversity
image_gen = ImageDataGenerator(rotation_range=20, # rotate the image 20 degrees
								width_shift_range=0.10, # Shift the pic width by a max of 5%
								height_shift_range=0.10, # Shift the pic height by a max of 5%
								rescale=1/255, # Rescale the image by normalzing it.
								shear_range=0.1, # Shear means cutting away part of the image (max 10%)
								zoom_range=0.1, # Zoom in by 10% max
								horizontal_flip=True, # Allo horizontal flipping
								fill_mode='nearest' # Fill in missing pixels with the nearest filled value
								)

image_gen.flow_from_directory(train_path)
image_gen.flow_from_directory(test_path)

#Creating the model

model = Sequential()

model.add(Conv2D(filters=32, kernel_size=(3,3),input_shape=image_shape, activation='relu',))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(filters=64, kernel_size=(3,3),input_shape=image_shape, activation='relu',))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(filters=64, kernel_size=(3,3),input_shape=image_shape, activation='relu',))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())

model.add(Dense(128, activation = 'relu'))

#adding dropout to avoid overfitting
model.add(Dropout(0.5))

model.add(Dense(1, activation = 'sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

#setting earlt stop to avoid overfitting and batch size to reduce training time
early_stop = EarlyStopping(monitor='val_loss',patience=2)
batch_size = 32

train_image_gen = image_gen.flow_from_directory(train_path, target_size=image_shape[:2],color_mode='rgb',
												batch_size=batch_size, class_mode='binary')

test_image_gen = image_gen.flow_from_directory(test_path, target_size=image_shape[:2],color_mode='rgb',
												batch_size=batch_size, class_mode='binary',shuffle = False)

results = model.fit_generator(train_image_gen,epochs=20,validation_data=test_image_gen,callbacks=[early_stop])

#Evaluating the model

losses = pd.DataFrame(model.history.history)
losses[['loss','val_loss']].plot()
plt.show()
