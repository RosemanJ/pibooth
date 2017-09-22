# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

def GetDateTimeString():
    dt = str(datetime.datetime.now()).split(".")[0]
    clean = dt.replace(" ","_").replace(":","_")
    return clean

def GetBackground(bgNumber):
    # bgImage = './backgrounds/' + str(new_img_nums[bgNumber]) + '.jpg'
    bgImage = '/home/pi/pibooth/backgrounds/space.jpg'
    return cv2.imread(bgImage)

def GetImage(bg, frame):
    # ret, frame = cam.read()

    sensitivity = 1 # play with sensitivity to get rid of noise...
    lowerRange = np.array([0, 0, 255 - sensitivity]) # this is currently set to white
    upperRange = np.array([255, sensitivity, 255]) # this is currently set to white

    #Mask the green screen
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    image_mask = cv2.inRange(hsv, lowerRange, upperRange)
    bg_mask = cv2.bitwise_and(bg, bg, mask = image_mask)
    fg_mask = cv2.bitwise_and(frame, frame, mask = cv2.bitwise_not(image_mask))
    img = cv2.add(bg_mask, fg_mask)

    return img

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# options for countdown timer
fontFace = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
thickness = 4
countdownSeconds = 5
displayPhotoSeconds = 5

# countdown to snapshot
clicked = False
clickedTime = {}

# backgrounds
new_img_nums = random.sample(range(1,9), 4)
bgNumber = 0
bg = GetBackground(bgNumber)

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array

	maskedImg = GetImage(bg, image) #get masked image from webcam

	# show the frame
	# cv2.imshow("Frame", image)
	cv2.imshow("Frame", maskedImg)
	# key = cv2.waitKey(1) & 0xFF
	key = cv2.waitKey(1)

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

    if clicked == True : # if countdown timer started
        elapsed = datetime.datetime.now() - clickedTime
        secs = int(elapsed.total_seconds())
        if secs > countdownSeconds : # if five seconds are up, save the current image
            clicked = False
            cv2.imwrite('/home/pi/pibooth/newImages/img_' + GetDateTimeString() + '.jpg',maskedImg)
            # cv2.imwrite('./newImages/img_' + GetDateTimeString() + '.jpg',img)
            cv2.imshow('Frame',maskedImg)
            time.sleep(displayPhotoSeconds) # show the photo for 5 seconds
            bgNumber += 1
            bg = GetBackground(bgNumber) # get a new background
        else : # show the countdown timer
            if secs - 5 == 1:
                text = 'Say cheese!'
            else:
                text = str(5 - secs) + "..."
            textSize, base = cv2.getTextSize(text, fontFace, fontScale, thickness)
            textWidth = int((width - textSize[0]) / 2)
            textHeight = int((height + textSize[1]) / 2)
            cv2.putText(img, text, (textWidth, textHeight), fontFace, fontScale, (255, 255, 255), thickness)
	# if the `q` key was pressed, break from the loop
	# if key == ord("q"):
	# 	break
	elif key == 27:
		break
	elif key == 32:
		clickedTime = datetime.datetime.now()
		clicked = True
    elif bgNumber == 4:
        # assemble photos into strip
        # print strip
        # reset app
        break
