#handles image capture
# capture_image is taken from one of the python examples
# earlier in the year

import subprocess
import cv2

IMAGE_PATH = "images/captured_image.jpg"
RESOLUTION = "640x480"       

def capture_image(path: str):
    # -S 2 skips a couple frames so exposure settles faster
    subprocess.run(["fswebcam", "-r", RESOLUTION, "-S", "2", "--no-banner", path], check=True)
    #return ""

def final_img():
    capture_image(IMAGE_PATH)
    
    # taken from https://pyimagesearch.com/2021/01/20/opencv-flip-image-cv2-flip/
    image = cv2.imread(IMAGE_PATH)

    # flip the image horizontally
    flipped = cv2.flip(image, 1)
    # write image to dir
    cv2.imwrite("flipped.jpg", flipped)
    # return the path of the final image
    # i'm not entirely sure if this is ever used
    # was intended if there was ever variable file outputs
    return "flipped.jpg"
