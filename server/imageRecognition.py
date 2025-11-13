from ollama import generate

import base64
import cv2
from flask import jsonify
import os

llmModel = "gemma3:4b"
imgPath = "images/frame.png"

#1 = 480x270
#2 = 960x540
#3 = 1440x810
#4 = 1920x1080
factor = 4
inputRes = (480 * factor, 270 * factor)

cam =  cv2.VideoCapture(0)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

#TODO: move to json file instead
initPrompt = "Your response will be read aloud to a visually-impaired user. Only speak in second-person."
endingPrompt = "Output exclusively your response to the user without any pretext. Do not use any special characters, except for common punctuation."

descImg = initPrompt + "Describe the scene in 1 sentence. Prioritize important details." + endingPrompt
readTxt = "Extract any text from the photo to be spoken aloud to to the user. Prices short be shortened. ($5.00 becomes 5 dollars). If you cannot reliably complete your task, output \"FAIL\" and nothing else." + endingPrompt
descObj = "Output only one word. Describe the object in front of you." + endingPrompt

# func modified from https://github.com/ollama/ollama-python/issues/283 user: pnmartinez
def describeImage(imgData, llmPrompt):
    response = generate(
        model=llmModel,
        prompt= llmPrompt,
        images=[imgData],  # Pass base64 encoded image data
        options={"temperature": 0.1},  # "imagination" of the ai response
        keep_alive= 600
    )
    caption = response["response"].strip()
    return caption
    

def imgToB64(imgPath):
    with open(imgPath, "rb") as img_file:
        img_data = img_file.read()

    return base64.b64encode(img_data).decode("utf-8")

#scale image down.
def resizeImage(imgPath):
    img = cv2.imread(imgPath)
    img = cv2.resize(img, inputRes)
    cv2.imwrite("images/frame.png", img)

def extractTextFromServer(imgPath):
    b64 = imgToB64(imgPath)
    return describeImage(b64, readTxt)

def describeImageFromServer(imgPath):
    b64 = imgToB64(imgPath)
    return describeImage(b64, descImg)

def describeObjectFromServer(imgPath):
    b64 = imgToB64(imgPath)
    return describeImage(b64, descObj)