import cv2, os, numpy as np
from glob import glob

def process(name):
	if (name == "test"):
		frame = cv2.imread("img/test/test.jpg")
		if frame is not None:
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			lower_brown = np.array([0,0,50])
			higher_brown = np.array([140,255,255])
			mask = cv2.inRange(hsv , lower_brown , higher_brown)
			mask = cv2.medianBlur(mask,9)
			res = cv2.bitwise_and(frame, frame, mask = mask)
			os.remove("img/test/test.jpg")
			cv2.imwrite("img/test/test.jpg", res)

	elif (name == "train"):
		imgs = glob("img/train/*.*")
		for img in imgs:
			frame =  cv2.imread(img)
			if frame is not None:
				hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
				lower_brown = np.array([20,40,100])
				higher_brown = np.array([70,255,255])
				mask = cv2.inRange(hsv , lower_brown , higher_brown)
				mask = cv2.medianBlur(mask,9)
				res = cv2.bitwise_and(frame, frame, mask = mask)
				os.remove(img)
				cv2.imwrite(img, res)

	else:
		print "Sorry Dude you are not going to get anything from here"
