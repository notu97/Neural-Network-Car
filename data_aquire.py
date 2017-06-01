import pygame
import sys
import serial
import time
import cv2
import urllib
import numpy as np
import os

def connectArduino(port='/dev/rfcomm1'):
    serArduino = serial.Serial(port, baudrate=9600, parity=serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
    serArduino.close()
    serArduino.open()
    if not serArduino.isOpen():
        print "Error Opening"
    else:
        time.sleep(1)
        print 'Arduino Connected'
        return serArduino

bytes = ''

def write_image(key,idx, img):
        cv2.imwrite('/home/shiladitya/Desktop/NNRCar/data/'+str(idx)+key+'.jpg',img)
    
Arduino = connectArduino()



#Setup PYGAME WINDOW
pygame.init()
pygame.display.set_caption('Enter keystrokes in this Window')
size = [300, 200]
screen = pygame.display.set_mode(size)
stream=urllib.urlopen('http://192.168.43.1:8080/video?.mjpeg')
idx = 0;
bytes = ''
while True:
    bytes += stream.read(1024)
    # 0xff 0xd8 is the starting of the jpeg frame
    a = bytes.find('\xff\xd8')
    # 0xff 0xd9 is the end of the jpeg frame
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        os.system ( 'clear' )
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        # Decoding the byte stream to cv2 readable matrix format
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            Arduino.close()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                write_image('l',idx,i)
                Arduino.write('l')
                idx = idx + 1
                print("Left Turn")
            if event.key == pygame.K_RIGHT:
                write_image('r',idx,i)
                Arduino.write('r')
                idx = idx + 1
                print("Right Turn")
            if event.key == pygame.K_UP:
                write_image('f',idx,i)
                Arduino.write('f')
                idx = idx + 1
                print("Forward")
            if event.key == pygame.K_DOWN:
                write_image('b',idx,i)
                Arduino.write('b')
                idx = idx + 1
                print("Backward")
            if event.key == pygame.K_s:
                write_image('s',idx,i)
                Arduino.write('s')
                idx = idx + 1 
                print("Stop")
        if event.type == pygame.KEYUP:
            Arduino.write('s') 
            print("Stop")
