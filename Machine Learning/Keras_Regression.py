import tensorflow as tf
import pandas as pd
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense


sample_data = pd.read_csv('concrete_data.csv')
sample_data.head()

sample_data.shape
sample_data.describe()
sample_data.isnull().sum()


sample_data_cols = sample_data.columns

# selecting predictors as all columns but result column
predictors = sample_data[sample_data_cols[sample_data_cols != 'Strength']] 
target = sample_data['Strength'] # Strength column as result

predictors.head()
target.head()

predictors_norm = (predictors - predictors.mean()) / predictors.std()
predictors_norm.head()
n_cols = predictors_norm.shape[1] # number of predictors

# define regression model
def regression():
    # create model
    model = Sequential()
    model.add(Dense(50, activation='relu', input_shape=(n_cols,)))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(1))
    
    # compile model
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# build the model
model = regression()

# fit the model
model.fit(predictors_norm, target, validation_split=0.3, epochs=100, verbose=2)