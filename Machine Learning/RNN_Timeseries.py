#predicting future sales based on sales data from RSCCASN.csv dataset, which should be located at the same directory


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.callbacks import EarlyStopping


#Reading and plotting data
df = pd.read_csv('RSCCASN.csv',index_col='DATE',parse_dates=True)
print(df.head())
df.plot(figsize=(12,8))
plt.show()

#performing train test split
test_size = 24
test_ind = len(df)- test_size #indicator where test dataset starts

train = df.iloc[:test_ind]
test = df.iloc[test_ind:]

#scaling data
scaler = MinMaxScaler()
# WE ONLY FIT TO TRAININ DATA, OTHERWISE WE ARE CHEATING ASSUMING INFO ABOUT TEST SET
scaler.fit(train)

scaled_train = scaler.transform(train)
scaled_test = scaler.transform(test)

#creating timseries generator to predict values 12 months ahead
prediction_range = 12
generator = TimeseriesGenerator(scaled_train, scaled_train, length=prediction_range, batch_size=1)

#creating the model

n_features = 1
model = Sequential()
model.add(LSTM(150, activation = 'relu',input_shape=(prediction_range, n_features)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

#early stopping to avoid overfitting and try to limit training time
early_stop = EarlyStopping(monitor='val_loss',patience=2)

validation_generator = TimeseriesGenerator(scaled_test,scaled_test, length=prediction_range, batch_size=1)
model.fit_generator(generator,epochs=20, validation_data=validation_generator, callbacks=[early_stop])


#Evaluating performance
losses = pd.DataFrame(model.history.history)
losses.plot()
plt.show()
#seems like it is ok to train just for 7 or 8 epochs. We'll use it when predicting future timestamps


test_predictions = []

first_eval_batch = scaled_train[-prediction_range:]
current_batch = first_eval_batch.reshape((1, prediction_range, n_features))

for i in range(len(test)):

	# get prediction 1 time stamp ahead ([0] is for grabbing just the number instead of [array])
	current_pred = model.predict(current_batch)[0]
	# store prediction
	test_predictions.append(current_pred) 
	# update batch to now include prediction and drop first value
	current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)

#reversing scaling
true_predictions = scaler.inverse_transform(test_predictions)
#predicting results for test set range
test['Predictions'] = true_predictions

test.plot(figsize=(12,8))
plt.show()

#retraining for future predictions
full_scaler = MinMaxScaler()
scaled_full_data = full_scaler.fit_transform(df)

generator = TimeseriesGenerator(scaled_full_data, scaled_full_data, length=prediction_range, batch_size=1)

model.fit_generator(generator,epochs=8)

#performing prediction for 12 months ahead
forecast = []
# Replace periods with forecast period
periods = 12

first_eval_batch = scaled_full_data[-prediction_range:]
current_batch = first_eval_batch.reshape((1, prediction_range, n_features))

for i in range(periods):

	current_pred = model.predict(current_batch)[0]
	# store prediction
	forecast.append(current_pred) 
	# update batch to now include prediction and drop first value
	current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)

forecast = scaler.inverse_transform(forecast)

#creating indexing for future predictions: monthly for 'periods' time ahead
forecast_index = pd.date_range(start='2019-11-01',periods=periods,freq='MS')
#storing them to the dataframe
forecast_df = pd.DataFrame(data=forecast,index=forecast_index,columns=['Forecast'])


#plotting
ax = df.plot()
forecast_df.plot(ax=ax)
plt.show()
