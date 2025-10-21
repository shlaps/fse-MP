import subprocess
import base64
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

def to_data_url(path: str) -> str:
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"
    
    
def main():
    capture_image(IMAGE_PATH)
    time.sleep(3)
    
    # https://pyimagesearch.com/2021/01/20/opencv-flip-image-cv2-flip/
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", type=str, default=IMAGE_PATH, help="path to the input image")
    
    args = vars(ap.parse_args())
    image = cv2.imread(args["image"])

    # flip the image horizontally
    flipped = cv2.flip(image, 1)
    cv2.imwrite("flipped.jpg", flipped)
    time.sleep(3)
	
	
	
	  
if __name__ == "__main__":
    main()
