import cv2, time, os
import numpy as np
from glob import glob

def training(name):

    # defining some var
    cons_t = 0
    aspect_ratio_t = 0
    extent_t = 0
    solidity_t = 0

    # opening txt file to write results
    fl = open('img/result.txt', 'a')

    # Finding image set
    paths = glob("img/train/*.*")

    if (len(paths) != 0):
        paths
        # Reading Image for training
        for path in paths:
            i = 0
            j = 0
            temp = 100
            img = cv2.imread(path,0)
            img = cv2.medianBlur(img,19)
            im2,contours,hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            # Finding biggest contourArea
            for cnt in contours:
                area_t = cv2.contourArea(cnt)
                if (temp < area_t):
                    j = i
                i = i + 1

            # Defining cnt as biggest contour
            print i, j
            cnt = contours[j]

            # finding area/perimeter^2
            peri = cv2.arcLength(cnt,0)
            area = cv2.contourArea(cnt)
            cons = (peri**2)/area

            # To find aspect_ratio
            (x,y),(MA,ma),angle = cv2.fitEllipse(cnt)
            aspect_ratio = ma/MA

            # to find ectent
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            l = ((box[0][0]-box[1][0])**2 + (box[0][1]-box[1][1])**2)**.5
            w = ((box[0][0]-box[3][0])**2 + (box[0][1]-box[3][1])**2)**.5
            rect_area = w*l
            extent = float(area)/rect_area

            # solidity
            area = cv2.contourArea(cnt)
            hull = cv2.convexHull(cnt)
            hull_area = cv2.contourArea(hull)
            solidity = float(area)/hull_area

            cons_t += cons
            extent_t += extent
            solidity_t += solidity
            aspect_ratio_t += aspect_ratio

            # removing images
            os.remove(path)

        # Writing results tp the file
        fl.write(str(cons_t/len(paths)) +  " " + str(aspect_ratio_t/len(paths)) + " " + str(solidity_t/len(paths)) + " " + str(extent_t/len(paths))+ " " + str(name) + "\n")
        return "Successfully trained"

    else:
        return "Not any image file is there"

    fl.close()
