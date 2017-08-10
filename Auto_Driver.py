# This code performs the auto-navigation function and guides the car on its own
#All the modules
import cv2
import pygame
import sys
import serial
import time
import urllib
import numpy as np
import os
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD,Adagrad
from keras.utils import np_utils
from keras.models import model_from_json
#End of modules


# In[9]:

#All the defination comes here
def connectArduino(port='/dev/rfcomm1'):
    serArduino = serial.Serial(port, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
    serArduino.close()
    serArduino.open()
    if not serArduino.isOpen():
        print "Error Opening"
    else:
        time.sleep(1)
        print 'Arduino Connected'
        return serArduino
def preprocess(img):
    #cv2.imshow("Original",img)
    img = img[80:,:]
    ret,thresh1 = cv2.threshold(img,150,255,cv2.THRESH_BINARY)
    
    kernel = np.ones((5,5),np.uint8)
    closing = cv2.morphologyEx(thresh1, cv2.MORPH_CLOSE, kernel)
    #cv2.imshow("Thresh",closing)
    #cv2.waitKey(1)
    #cv2.destroyAllWindow()
    closing = cv2.pyrDown(closing)
    closing = cv2.pyrDown(closing)
    return closing

#All defination Over


# In[10]:

#Load the saved keras model

#Load json file
print('Loading the Neural Network Model')
json_file = open('model.json','r')
model = json_file.read()
json_file.close()
model = model_from_json(model)
model.load_weights("model.h5")
print('Model Successfully Loaded')


# In[ ]:

cap = cv2.VideoCapture()
Arduino = connectArduino()
#Opening the Link
cap.open("http://192.168.43.1:8080/video?.mjpeg")
while True:
    
    #Arduino.write('s')
    #Capture frame by frame
    ret,frame = cap.read()
    #Displaying the resulting frame
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    frame_process = preprocess(frame)
    print frame_process.shape
    input_img = frame_process.flatten()
    input_img = input_img.reshape((1,600))
    #Make Prediction
    direction = model.predict_classes(input_img, batch_size=100, verbose=1)
    print direction
    Arduino.write('s') 
    #Send Command to Arduino
    if(direction==0): Arduino.write('f')
    elif(direction==1): Arduino.write('l')
    else: Arduino.write('r')

    print('Command Sent')
       
    #Displaying Views on Screen    
    #cv2.imshow('Captured Image',frame)
    #cv2.imshow('Processed Image',frame_process)
    #os.system('clear')
    #cv2.waitKey(0)
    
#    print "Press q to exit"
#    if (cv2.waitKey(1) & OxFF == ord('q')):
#        break
    #cap.release()
    #cv2.destroyAllWindow()


# In[ ]:



