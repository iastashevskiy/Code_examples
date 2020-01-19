import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D, Flatten
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import classification_report,confusion_matrix

from tensorflow.keras.datasets import mnist

# load data
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# reshape to be samples, height, width, color channels
X_train = X_train.reshape(X_train.shape[0], 28, 28, 1).astype('float32')
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1).astype('float32')

# normalize data. Maximum level is 255, so we'll devide by 255
X_train = X_train / 255 
X_test = X_test / 255 

#transforming continious data into classes
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

num_classes = y_test.shape[1] # number of categories

# function for model creation
def convolutional_model():
	
	model = Sequential()
	model.add(Conv2D(filters=16, kernel_size = (5, 5), activation = 'relu', input_shape=(28, 28, 1)))
	model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
	
	model.add(Conv2D(filters = 8, kernel_size = (2, 2), activation='relu'))
	model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
	
	model.add(Flatten())
	model.add(Dense(100, activation='relu'))
	model.add(Dense(num_classes, activation='softmax'))
	
	# Compile model
	model.compile(optimizer='adam', loss='categorical_crossentropy',  metrics=['accuracy'])
	return model

#constructing a model with an early stop to avoid overfitting	
model = convolutional_model()
early_stop = EarlyStopping(monitor='val_loss',patience=2)
model.summary()
# fitting the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, verbose=2, callbacks = [early_stop])

# evaluating the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: {} \n Error: {}".format(scores[1], 100-scores[1]*100))

losses = pd.DataFrame(model.history.history)
losses[['accuracy','val_accuracy']].plot()
plt.show()
losses[['loss','val_loss']].plot()
plt.show()

