import subprocess
import sys
import os
import time

import argparse	
import cv2

IMAGE_PATH = "captured_image.jpg"
RESOLUTION = "640x480"       

def capture_image(path: str):
    # -S 2 skips a couple frames so exposure settles faster
    subprocess.run(["fswebcam", "-r", RESOLUTION, "-S", "2", "--no-banner", path], check=True)
    #return ""

def final_img():
    capture_image(IMAGE_PATH)
    
    # https://pyimagesearch.com/2021/01/20/opencv-flip-image-cv2-flip/
    image = cv2.imread(IMAGE_PATH)

    # flip the image horizontally
    flipped = cv2.flip(image, 1)
    cv2.imwrite("flipped.jpg", flipped)
    return "flipped.jpg"
