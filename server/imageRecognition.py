from ollama import generate

import base64
import cv2
import camtest
from flask import jsonify
from threading import Thread
import os

#server_thread = Thread(target=main.run, daemon=True)
#server_thread.start()

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
initPrompt = "Your response will be read aloud to a visually-impaired user. "
endingPrompt = "Output exclusively your response to the user without any pretext. Do not use any special characters, except for common punctuation."
descImg = initPrompt + "Describe the image captured from the device provided to the user. Warn the user of any danger or obstacles first, if present. Otherwise, say nothing of the lack of danger/obstacles. Feel free to make reasonable assumptions about the danger posed to the user, if present. Transcribe or summarize any text which might be important to the user. Keep your response brief, but with concise detail. Read any text to the user you feel is important." + endingPrompt
readTxt = initPrompt + "Extract any text from the photo to be spoken aloud to to the user. Prioritize accuracy. If you cannot reliably complete your task, output \"[FAIL]\" and nothing else." + endingPrompt

# func modified from https://github.com/ollama/ollama-python/issues/283 user: pnmartinez
def describeImage(imgData, llmPrompt):
    try:
        pass
    except:
        pass
    try:
        response = generate(
            model=llmModel,
            prompt= llmPrompt,
            images=[imgData],  # Pass base64 encoded image data
            options={"temperature": 0.1},  # "imagination" of the ai response
            keep_alive= 600
        )
        caption = response["response"].strip()
        return caption
    except:
        return jsonify({"error": "Model Failure"}), 400
    

def imgToB64(imgPath):
    with open(imgPath, "rb") as img_file:
        img_data = img_file.read()

    return base64.b64encode(img_data).decode("utf-8")

#scale image down.
def resizeImage(imgPath):
    img = cv2.imread(imgPath)
    img = cv2.resize(img, inputRes)
    cv2.imwrite("images/frame.png", img)

#depeciated
def describeImageFromCamera():
    camtest.takePhoto(cam)
    resizeImage(imgPath)
    b64 = imgToB64(imgPath)
    print(describeImage(b64, descImg))
#depeciated
def extractTextFromCamera():
    camtest.takePhoto(cam)
    resizeImage(imgPath)
    b64 = imgToB64(imgPath)
    print(describeImage(b64, readTxt))

def extractTextFromServer(imgPath):
    b64 = imgToB64(imgPath)
    return describeImage(b64, readTxt)

def describeImageFromServer(imgPath):
    b64 = imgToB64(imgPath)
    return describeImage(b64, descImg)

def main():
    os.system('cls')
    print("1) Describe webcam image.\n2) Extract text\n3) Continuously describe webcam image until quit\nx) Quit")
    userIn = int(input("Input : "))
    while (userIn < 4 and userIn > 0):
        if (userIn == 1):
            describeImageFromCamera()
        elif (userIn == 2):
          extractTextFromCamera()
        elif (userIn == 3):
            while True:
                describeImageFromCamera()
        print("1) Describe webcam image.\n2) Extract text\n3) Continuously describe webcam image until quit\nx) Quit")
        userIn = int(input("Input : "))



