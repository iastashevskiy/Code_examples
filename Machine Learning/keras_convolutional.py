import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from keras.layers.convolutional import Conv2D 
from keras.layers.convolutional import MaxPooling2D 
from keras.layers import Flatten 

from keras.datasets import mnist

# load data
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# reshape to be [samples][pixels][width][height]
X_train = X_train.reshape(X_train.shape[0], 28, 28, 1).astype('float32')
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1).astype('float32')

# normalize data
X_train = X_train / 255 
X_test = X_test / 255 

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

num_classes = y_test.shape[1] # number of categories


def convolutional_model():
	
	# create model
	model = Sequential()
	model.add(Conv2D(16, (5, 5), activation='relu', input_shape=(28, 28, 1)))
	model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
	
	model.add(Conv2D(8, (2, 2), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
	
	model.add(Flatten())
	model.add(Dense(100, activation='relu'))
	model.add(Dense(num_classes, activation='softmax'))
	
	# Compile model
	model.compile(optimizer='adam', loss='categorical_crossentropy',  metrics=['accuracy'])
	return model

	
model = convolutional_model()

# fit the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, verbose=2)

# evaluate the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: {} \n Error: {}".format(scores[1], 100-scores[1]*100))