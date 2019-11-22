#Part 1: Libraries
import serial                    # for reading data from Arduino
import pandas as pd              # for data manipulation
import time                      # for time capturing
import csv                       # for csv file creation


#Part 2 get values
# Connect to Arduion and get Data, MAY NEED TO MANUALLY CHANGE VALUES
arduinoData = serial.Serial('/dev/cu.usbmodem141301', 115200) # read serial info from arduino


#Part 3 Initialization
# Initialize empy Lists, for new or resetting CSV
y_data = []
FS0_data = []   # empty array for sensor 0 data
FS1_data = []   # empty array for sensor 1 data
FS2_data = []   # empty array for sensor 2 data
FS3_data = []   # empty array for sensor 3 data
#FS4_data = []   # empty array for sensor 4 data
#FS5_data = []   # empty array for sensor 5 data
#FS6_data = []   # empty array for sensor 6 data
#FS7_data = []   # empty array for sensor 7 data
#FS8_data = []   # empty array for sensor 8 data

#plt.ion()       # for live data
cnt = 0         # counter
count = 0
tempt = 0
pause_time = 1.5
iteration = 0

#Part 4: Get Data
# Continuous Loop to make CSV file. Let run first to get timings right
with open('input_2x2_softdylan2.csv', 'a', newline = "") as X: # change 'w' to 'a' to append
    writer = csv.writer(X) # writes to input csv
    #1x1
    #writer.writerow(['Sensor 0', 'Time']) # COMMENT OUT THIS LINE IF APPENDING, MAKES TITLES
    #2x2
    writer.writerow(['Sensor 0', 'Sensor 1', 'Sensor 2', 'Sensor 3', 'Time'])
    #3x3
    #writer.writerow(['Sensor 0', 'Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5', 'Sensor 6', 'Sensor 7', 'Sensor 8', 'Time'])
    with open('output_2x2_softdylan2.csv', 'a', newline = "") as Y: # change 'w' to 'a' to append
        label = csv.writer(Y) # writes to output csv
        label.writerow(['action', 'Length']) # COMMENT OUT THIS LINE IF APPENDING, MAKES TITLES
        # Continuously Running Loop
        now = time.time()
        while True: # runs until program is manually stopped

            # time at the beginning of loop and future time 2 seconds from the start
            start = time.time()
            future = start + 1

            #When data is not being read
            while(arduinoData.inWaiting()==0):  # if there is not data
                #if certain amount of time passes with no value, ask what just happened
                if time.time() > future:
                    value = input('what kind of data was that?')
                    now = time.time() # get time of input
                    temp = count - cnt # creates length of data just entered
                    cnt = 0
                    print(value) # test if everything is going correctly
                    #write what just happened to the csv file
                    for i in range(temp, count):
                        # write action and length of data into output
                        label.writerow([value, count])
                    count = 0
                    time.sleep(pause_time)
                    iteration += 1
                    print('Iteration: ', iteration)
                    print('done')
                else:
                    pass # while data is being read ignore above

            # Reads lines from arduino
            arduinoRow = arduinoData.readline() # for all data read Serial Lines
            cnt = cnt + 1
            count = count + 1

            # Split Data at "," as controlled by Arduino code
            dataArray = arduinoRow.split(b',')  # slit data at ' ' defined in C++ program
             # test to make sure all is well


            FS0 = float(dataArray[0])   # turn string data into number
            FS1 = float(dataArray[1])   # turn string data into number
            FS2 = float(dataArray[2])   # turn string data into number
            FS3 = float(dataArray[3])   # turn string data into number
            #FS4 = float(dataArray[4])   # turn string data into number
            #FS5 = float(dataArray[5])   # turn string data into number
            #FS6 = float(dataArray[6])   # turn string data into number
            #FS7 = float(dataArray[7])   # turn string data into number
            #FS8 = float(dataArray[8])   # turn string data into number

            print(FS0, FS1, FS2, FS3)
            FS0_data.append(FS0)        # append data from sensor 0
            FS1_data.append(FS1)        # append data from sensor 1
            FS2_data.append(FS2)        # append data from sensor 2
            FS3_data.append(FS3)        # append data from sensor 3
            #FS4_data.append(FS4)        # append data from sensor 4
            #FS5_data.append(FS5)        # append data from sensor 5
            #FS6_data.append(FS6)        # append data from sensor 6
            #FS7_data.append(FS7)        # append data from sensor 7
            #FS8_data.append(FS8)        # append data from sensor 8

            #1X1
            # write above info to data, Increase depending on number of sensores same for above
            #writer.writerow([FS0_data[len(FS0_data)-1], (time.time() - now - pause_time)])

            #2X2
            # write above info to data, Increase depending on number of sensores same for above
            writer.writerow([FS0_data[len(FS0_data)-1], FS1_data[len(FS1_data)-1], FS2_data[len(FS2_data)-1], FS3_data[len(FS3_data)-1], (time.time() - now - pause_time)])

            #3X3
            # write above info to data, Increase depending on number of sensores same for above
            #writer.writerow([FS0_data[len(FS0_data)-1], FS1_data[len(FS1_data)-1], FS2_data[len(FS2_data)-1], FS3_data[len(FS3_data)-1], FS4_data[len(FS4_data)-1], FS5_data[len(FS5_data)-1], FS6_data[len(FS6_data)-1], FS7_data[len(FS7_data)-1], FS8_data[len(FS8_data)-1], (time.time() - now - pause_time)])


#Part 5: View Data
# View data just created
#inputdata = pd.read_csv('input_2x2_10_8_7pm.csv')
#outputdata = pd.read_csv('output_2x2_10_8_7pm.csv')


##############################################################################################################################
#import threading
#import numpy                     # Array creation and Manipulation
#import matplotlib.pyplot as plt  # plot data
#from drawnow import *            # Live Data
