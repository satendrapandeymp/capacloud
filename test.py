import cv2, time, re, os
import numpy as np

def testing():
    # defining some var
    i = 0
    j = 0
    temp = 100

    # Reading Image
    img = cv2.imread("img/test/test.jpg",0)

    # checking if img read Successfully
    if img is not None:
        img = cv2.medianBlur(img,7)
        im2,contours,hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Finding biggest contourArea
        for cnt in contours:
            area_t = cv2.contourArea(cnt)
            if (temp < area_t):
                j = i
            i = i + 1

        # Defining cnt as biggest contour
        cnt = contours[j]

        # finding area/perimeter^2
        peri = cv2.arcLength(cnt,0)
        area = cv2.contourArea(cnt)
        cons = (peri**2)/(area)

        # To find aspect_ratio
        (x,y),(MA,ma),angle = cv2.fitEllipse(cnt)
        aspect_ratio = ma/(MA)

        # to find extent
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        l = ((box[0][0]-box[1][0])**2 + (box[0][1]-box[1][1])**2)**.5
        w = ((box[0][0]-box[3][0])**2 + (box[0][1]-box[3][1])**2)**.5
        rect_area = w*l
        extent = float(area)/(rect_area)

        # solidity
        area = cv2.contourArea(cnt)
        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        solidity = float(area)/(hull_area)
        os.remove("img/test/test.jpg")

        # opening result file to get data of different leafs
        fl = open('img/result.txt', 'r')
        raw = fl.read()

        # processing for useful data from txt file
        datas = re.split("\n", raw)

        # cheking if file is not empty
        if (len(datas) > 1):
            # creating an impty array to store result
            result = []
            small = 0
            temp = 10
            # now starting to find distances from each cateogary of leaf
            for data in datas:
                val = re.split(" ", data)
                if (len(val) == 5):
                    cons_t = float(val[0])
                    aspect_ratio_t = float(val[1])
                    solidity_t = float(val[2])
                    extent_t = float(val[3])
                    leaf_name = val[4]
                    ds = (( 2* ((cons-cons_t)/cons_t)**2 + ((solidity-solidity_t)/solidity_t)**2 + ((extent-extent_t)/extent_t)**2 + 2 * ((aspect_ratio-aspect_ratio_t)/aspect_ratio_t)**2 )**.5)/6
                    if (ds<.15):
                        return "this leaf belongs to " + leaf_name + " cateogary"
                    elif(ds < temp):
                        small += 1
                        result.append(ds)
                        result.append(leaf_name)
                else:
                    if (float(result[2*(small-1)] < .2)):
                        return "this leaf belongs to " + str(result[2*(small-1)+1]) + " cateogary"
                    else:
                        return "closest leaf is belongs to " + str(result[2*(small-1)+1]) + " cateogary with an error of " + str(float( result[2*(small-1)])*100) + "%"
        else:
            return "We can't see any data in our database so please train first"
    else:
        return "We can't see a valid image for testing, for more see debug results"
