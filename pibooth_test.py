import numpy as np
import cv2
import datetime
from random import randint
import time
import logging

def GetDateTimeString():
    dt = str(datetime.datetime.now()).split(".")[0]
    clean = dt.replace(" ","_").replace(":","_")
    return clean

def GetBackground():
    # for a set of 4 images in a strip we need to keep track of the random nums already generated - no dupes!
    # new_img_nums = random.sample(range(1,9), 4)

    new_img_num = randint(1,9)
    # bgImage = '/home/pi/pibooth/backgrounds/' + str(new_img_num) + '.jpg'
    bgImage = './backgrounds/' + str(new_img_num) + '.jpg'
    return cv2.imread(bgImage)

def GetImage(bg):
    ret, frame = cap.read()

    logging.warning(frame)  # will print a message to the console

    #Mask the green screen
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    image_mask = cv2.inRange(hsv, np.array([40,50,50]), np.array([80,255,255]))
    bg_mask = cv2.bitwise_and(bg, bg, mask = image_mask)
    fg_mask = cv2.bitwise_and(frame, frame, mask = cv2.bitwise_not(image_mask))
    img = cv2.add(bg_mask, fg_mask)
    return img

#Setup WebCam
cap = cv2.VideoCapture(0)
width = 1920
height = 1080

cap.set(3, width)
cap.set(4, height)


bg = GetBackground()
img = GetImage(bg) #get masked image from webcam

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)

    key = cv2.waitKey(1) #check for keypress

    if key & 0xFF == ord('q'):
        break
    elif key & key == 27:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
