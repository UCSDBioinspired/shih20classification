# The purpose of this file is to test your model in real time

import time
import serial
import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from keras import backend as K

model = load_model('LSTM_2x2_10_8_7pm_emily4.h5')  # load model that you trained in LSTM_Creator

arduinoData = serial.Serial('/dev/cu.usbmodem141201', 115200) # make sure to change to correct arduino port

#Initializing data for live data manipulation
FS0_data = []   # empty array for sensor 0 data
FS1_data = []   # empty array for sensor 1 data
FS2_data = []   # empty array for sensor 2 data
FS3_data = []   # empty array for sensor 3 data


X_AR = []
cnt_AR = 0
X_AR_Scaled = []
dataArray = []

threshold = 6.0

dataArray = []
#Part 4: Important values you can change
timestep_AR =  60
features_AR = 4
count = 0
tempt = 0
cnt = 0
window_size = 30
iteration = 0
maxlen = 189 #same as maxlen from LSTM_Creator

arduinoData.flush()

now = time.time()
while True:

    start = time.time()
    future = start + .5

    dataArray = []
    m=0
    arduinoRow = arduinoData.readline() # for all data
    cnt = cnt + 1
    count = count + 1
    dataArray = arduinoRow.split(b',')  # slit data at ' ' defined in C++ program
    arduinoRow = []
    print(dataArray)


    if((float(dataArray[0]) >= 8.00 or float(dataArray[1]) >= 8.00 or float(dataArray[2]) >= 8.00 or float(dataArray[3]) >= 8.00)):

        FS0_AR = float(dataArray[0])   # turn string data into number
        FS1_AR = float(dataArray[1])   # turn string data into number
        FS2_AR = float(dataArray[2])   # turn string data into number
        FS3_AR = float(dataArray[3])   # turn string data into number

        FS0_data.append(FS0_AR)        # append data from sensor 0
        FS1_data.append(FS1_AR)        # append data from sensor 1
        FS2_data.append(FS2_AR)        # append data from sensor 2
        FS3_data.append(FS3_AR)        # append data from sensor 3

        iteration += 1

        X_AR.append([FS0_data[len(FS0_data)-1], FS1_data[len(FS1_data)-1], FS2_data[len(FS2_data)-1], FS3_data[len(FS3_data)-1]])#, (time.time() - now)])

    while((arduinoData.inWaiting()==0) and (iteration > 10) and (len(X_AR) >= 10)):#and not line and access and not key
         if(time.time() > future):
            print('enter')
            future = 0

            temp = count - cnt
            cnt = 0
            data_X = []
            data_X = pd.DataFrame(X_AR)
            #X_AR_scaled = sc.fit_transform(X_AR) #normalization on data

            L1 = []
            X_train_AR = []
            reshaped_X_AR = []
            S0_Ar = []
            S1_Ar = []
            S2_Ar = []
            S3_Ar = []

            S0_AR = data_X[0].values
            S1_AR = data_X[1].values
            S2_AR = data_X[2].values
            S3_AR = data_X[3].values

            S0_AR=np.pad(S0_AR,(0,maxlen-len(S0_AR)),'constant') #pad data to max length
            S1_AR=np.pad(S1_AR,(0,maxlen-len(S1_AR)),'constant')
            S2_AR=np.pad(S2_AR,(0,maxlen-len(S2_AR)),'constant')
            S3_AR=np.pad(S3_AR,(0,maxlen-len(S3_AR)),'constant')
            X_train_AR = [S0_AR, S1_AR, S2_AR, S3_AR]

            count = 0

            # reshape to same format as LSTM input
            reshaped_X_AR = np.array([np.transpose(np.asarray(X_train_AR, dtype = np.float32))])

            # prediction
            yhat = model.predict(reshaped_X_AR)

            # ANSWER
            yhat = np.array(yhat)

            print(yhat)


            FS0_data = []   # empty array for sensor 0 data
            FS1_data = []   # empty array for sensor 1 data
            FS2_data = []   # empty array for sensor 2 data
            FS3_data = []   # empty array for sensor 3 data

            T1_data = []
            cnt_AR = 0
            X_AR = []
            X_AR_scaled = []

            if (len(yhat) > 0):
                m = np.amax(yhat)
            else:
                m = 0
            arduinoData.flush()
            if(m > .50):
                biggest_value = yhat.argmax()

                if (biggest_value == 0):
                    print('poke bottom left')
                elif (biggest_value == 1):
                    print('poke bottom right')
                elif (biggest_value == 2):
                    print('poke top left')
                elif (biggest_value == 3):
                    print('poke top right')
                elif (biggest_value == 4):
                    print('poke center')
                elif (biggest_value == 5):
                    print('vertical rub down')
                elif (biggest_value == 6):
                    print('horizontal rub L to R')
                elif (biggest_value == 7):
                   print('vertical rub L top to bottom')
                elif (biggest_value == 8):
                    print('horizontal top rub L to R')
                elif (biggest_value == 9):
                    print('diagonal rub TL to BR')
            else:
                print('action not clear')

            now = time.time()
