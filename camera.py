import cv2,time, numpy as np, os
import paho.mqtt.client as mqtt

ip = "localhost"         # to send data through MQTT

def connect_cam(vend):

    # Opening video stream in opencv
    cap = cv2.VideoCapture(vend)

    # Make sure that it's opened before moving furthur
    num = 0
    cam_connected = True
    while(not cap.isOpened()):
        num +=1
        cap = cv2.VideoCapture(cam)                 # trying again
        if (num > 10):
            cam_connected = False
            break
        elif cap.isOpened():                          # Break if opened
            break

    # if camera opened then moving ahead
    while(cam_connected):

        # check if stopped from browser
        if os.path.isfile("static/3.jpg"):
            os.remove("static/3.jpg")
            break

        # if everything is okay then moving ahead
        ret, frame = cap.read()
        if ret:                                                         # If able to read image then moving ahead
            hight, width, c = frame.shape
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # For filtering of dead leaf colour
            lower_brown = np.array([15,0,100])
            higher_brown = np.array([35,150,200])
            mask = cv2.inRange(hsv , lower_brown , higher_brown)
            res = cv2.bitwise_and(frame, frame, mask = mask)
            # For getting the area
            hierarchy, contours, _ = cv2.findContours(mask, 1, 2)
            area = 0
            temp = 0
            flag = 0
            i = 0
            j = 0
            for cnt in contours:
                area_t = cv2.contourArea(cnt)
                area = area + area_t
                if (temp < area_t):
                    flag = 1
                    temp = area_t
                    j = i
                i = i + 1

            # for getting largest dead part centroid
            if (flag != 0):
                c = contours[j]
                M = cv2.moments(c)
                if (int(M['m00'] != 0)):
                    cY = int(M['m10']/M['m00'])
                    cX = int(M['m01']/M['m00'])

                """ for getting extreme points of the dead part and pointing by small circle
                extLeft = tuple(c[c[:, :, 0].argmin()][0])
                extRight = tuple(c[c[:, :, 0].argmax()][0])
                extTop = tuple(c[c[:, :, 1].argmin()][0])
                extBot = tuple(c[c[:, :, 1].argmax()][0])

                cv2.circle(res, extLeft, 20, (0, 0, 255), -1)
                cv2.circle(res, extRight, 20, (0, 255, 0), -1)
                cv2.circle(res, extTop, 20, (255, 0, 0), -1)
                cv2.circle(res, extBot, 20, (255, 255, 0), -1)
                """

                # drawing contour
                cv2.drawContours(res, [c], -1, (0, 255, 255), 5)

                # Printing centroid
                message = ""
                message = "Relative position of centroid " + str(cY - (width/2))  + ',' +  str((hight/2) - cX) + "    "

                # For filtering of total leaf colour
                lower_fore = np.array([40,0,0])
                higher_fore = np.array([65,255,255])
                mask1 = cv2.inRange(hsv , lower_fore , higher_fore)
                mask1 = cv2.medianBlur(mask1,15)
                res1 = cv2.bitwise_and(frame, frame, mask = mask1)

                # for getting the total leaf area
                hierarchy, contours, _ = cv2.findContours(mask1, 1, 2)
                area1 = 1
                for cnt in contours:
                    area1 = area1 + cv2.contourArea(cnt)

                results = area*100/area1
                message +=  "ratio = " + str(results) + '%'

                cv2.imwrite('static/1.jpg',frame)
                cv2.imwrite('static/2.jpg',res)



                try:
                    client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol="MQTTv31")
                    client.connect(ip, 1883, keepalive=60, bind_address="") #connect
                    client.loop_start() #start loop
                    client.publish("leaf", payload=message, qos=0, retain=False)
                    client.loop_stop()
                    client.disconnect()

                except Exception, e:
                    print e


            else:
                print 'No dead patches detected'

        else:
            print "Can't read frame"
            break
