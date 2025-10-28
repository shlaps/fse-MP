# modified from 
# https://stackoverflow.com/questions/34588464/python-how-to-capture-image-from-webcam-on-click-using-opencv#34588758

import cv2
import warnings

def takePhoto(cam):
    try:
        #cv2.namedWindow("Photo")
        ret, frame = cam.read()
    
        #cv2.imshow("Photo", frame)

        img_name = "images/frame.png"
        cv2.imwrite(img_name, frame)
        print("Frame written!")
    except:
        warnings.warn("Failed to grab frame")

def exit(cam):
    cam.release()
    #cv2.destroyAllWindows()