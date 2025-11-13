import imageCapture
import requests
from flask import jsonify
import cv2
import base64

def openImg(imgPath):
    with open(imgPath, "rb") as img_file:
        img_data = img_file.read()

    return img_data

path = "client/images/frame.png"
files = {'image': openImg(path)}



r = requests.post(url="http://127.0.0.1:5000/upload", files=files)
print(r.text)