import numpy as np
import cv2

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

bg = cv2.imread('./backgrounds/space.jpg', 1)
sensitivity = 1
lowerRange = np.array([0, 0, 255 - sensitivity])
upperRange = np.array([255, sensitivity, 255])

while (True):
  ret, frame = cam.read()
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  image_mask = cv2.inRange(hsv, lowerRange, upperRange)
  bg_mask = cv2.bitwise_and(bg, bg, mask = image_mask)
  fg_mask = cv2.bitwise_and(frame, frame, mask = cv2.bitwise_not(image_mask))

  cv2.imshow('Output', cv2.add(bg_mask, fg_mask))

  if cv2.waitKey(1) == 27:
    break

cv2.destroyAllWindows()
cam.release()
