import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D, Flatten
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import classification_report,confusion_matrix


#Downloading data into datasets
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

#Normalizing data
x_train = x_train/225
x_test = x_test/255

#transforming continious data into classes
y_cat_train = to_categorical(y_train,10)
y_cat_test = to_categorical(y_test,10)

#creating the model
model = Sequential()

model.add(Conv2D(filters=32, kernel_size=(4,4),input_shape=(32, 32, 3), activation='relu',))
model.add(MaxPool2D(pool_size=(2, 2)))

model.add(Conv2D(filters=32, kernel_size=(4,4),input_shape=(32, 32, 3), activation='relu',))
model.add(MaxPool2D(pool_size=(2, 2)))

model.add(Flatten())

model.add(Dense(256, activation='relu'))
model.add(Dense(10, activation='softmax'))

model.compile(loss='categorical_crossentropy',optimizer='rmsprop',metrics=['accuracy'])

#fitting the model with an early stop to avoid overfitting	
early_stop = EarlyStopping(monitor='val_loss',patience=3)
model.fit(x_train,y_cat_train,epochs=15,validation_data=(x_test,y_cat_test),callbacks=[early_stop])

#Evaluating results

losses = pd.DataFrame(model.history.history)
losses.head()

losses[['accuracy','val_accuracy']].plot()
plt.show()

losses[['loss','val_loss']].plot()
plt.show()

print(model.metrics_names)
print(model.evaluate(x_test,y_cat_test,verbose=0))

predictions = model.predict_classes(x_test)
print(classification_report(y_test,predictions))
confusion_matrix(y_test,predictions)

#giving a prediction

Random_image = x_test[random.randint(0, len(y_test))]
plt.imshow(Random_image)

model.predict_classes(my_image.reshape(1,32,32,3)) #reshaping as 1 colored image 32*32 pixels