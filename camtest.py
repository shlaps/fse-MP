# modified from 
# https://stackoverflow.com/questions/34588464/python-how-to-capture-image-from-webcam-on-click-using-opencv#34588758

import cv2

def takePhoto(cam):
    cv2.namedWindow("Photo")
    ret, frame = cam.read()

    if not ret:
        print("failed to grab frame")
        return
    
    cv2.imshow("Photo", frame)

    img_name = "opencv_frame_{}.png"
    cv2.imwrite(img_name, frame)
    print("{} written!".format(img_name))

def exit(cam):
    cam.release()
    cv2.destroyAllWindows()