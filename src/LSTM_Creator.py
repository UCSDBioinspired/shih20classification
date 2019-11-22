# The purpose of this file is to train a LSTM network with 2x2 sensor data.

import numpy as np # make arrays
import pandas as pd # import data to be used
from scipy import stats # import stats
from sklearn.preprocessing import LabelEncoder, OneHotEncoder # encode data
from sklearn.preprocessing import MinMaxScaler  # min/max to use normalization
from sklearn.model_selection import train_test_split # for splitting data
from matplotlib import pyplot
import csv

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import LSTM

np.random.seed(0)

# Importing and formatting the dataset
inputdata = pd.read_csv('inputbetter2.csv')
outputdata = pd.read_csv('outputbetter2.csv')

maxlen = max(outputdata['Length'].values) #padding array to this length
N_timesteps = outputdata['Length'].values[1]#20 # number of data points that the touch lasts for
N_features = 4 #number of features = number of sensors
i=0

# Create Training Data in the Way LSTM likes
X_train = []
y_train = []
for i in range(0, len(inputdata)-maxlen, N_timesteps):
    S0 = inputdata['Sensor 0'].values[i:i + N_timesteps]             # Get sensor 0 data
    S1 = inputdata['Sensor 1'].values[i:i + N_timesteps]             # Get sensor 1 data
    S2 = inputdata['Sensor 2'].values[i:i + N_timesteps]             # Get sensor 2 data
    S3 = inputdata['Sensor 3'].values[i:i + N_timesteps]             # Get sensor 3 data

    action = stats.mode(outputdata['action'][i:i + N_timesteps])# get label for data
    action = action[0][0] # gets action from list made in previous line

    S0=np.pad(S0,(0,maxlen-N_timesteps),'constant') #pad data to max length
    S1=np.pad(S1,(0,maxlen-N_timesteps),'constant')
    S2=np.pad(S2,(0,maxlen-N_timesteps),'constant')
    S3=np.pad(S3,(0,maxlen-N_timesteps),'constant')

    N_timesteps = outputdata['Length'].values[i+N_timesteps] #num of data points in next touch

    X_train.append(np.transpose(np.asarray([S0, S1, S2, S3],dtype = np.float32))) # append data point to input for LSTM
    y_train.append(action) #append data point to output for LSTM


reshaped_X_train = np.asarray(X_train) #put in array form for input to LSTM

# encoding of y data as dummy vars
y_train = np.asarray(pd.get_dummies(y_train), dtype = np.float32)

# Split Data. 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(reshaped_X_train, y_train, test_size = 0.2)


# Build the model using keras LSTM
regressor = Sequential() #create LSTM

Number_of_actions = 10; #number of output actions = 5 types of poke and 5 types of rub


nodes =85
# Add layers/ dropout regularization
regressor.add(Dense(nodes,kernel_initializer='random_uniform',bias_initializer='zeros'))
regressor.add(LSTM(nodes,return_sequences = True,input_shape = (maxlen, N_features)))
regressor.add(Dropout(0.2))

regressor.add(LSTM(nodes,return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(nodes,return_sequences = False))
regressor.add(Dropout(0.2))

# Add output layer, equal to amount of actions
regressor.add(Dense(units = Number_of_actions))
regressor.add(Activation('softmax'))

# Compile
regressor.compile(optimizer = 'adam', loss = 'categorical_crossentropy',metrics=['acc'])

# Fit the RNN to the Training set
history = regressor.fit(X_train, y_train, epochs = 50, batch_size = 32,validation_data=(X_test,y_test))

# plot loss over epochs to determine best number of epochs
pyplot.plot(history.history['loss'])
pyplot.plot(history.history['val_loss'])
pyplot.title('model train vs validation loss')
pyplot.ylabel('loss')
pyplot.xlabel('epoch')
pyplot.legend(['train', 'validation'], loc='upper right')
pyplot.show()

# SAVE MODEL
regressor.save('LSTM_2x2_10_8_7pm_emily8.h5')
