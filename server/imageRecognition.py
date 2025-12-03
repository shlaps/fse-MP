# this file does all the AI image recognition!!
# its largely powered by the amazing ollama API
# (and its python library)

#AI library
from ollama import generate

#other libraries
import base64
import cv2

# AI model. must be installed locally
llmModel = "gemma3:4b"
imgPath = "images/frame.png"

#1 = 480x270
#2 = 960x540
#3 = 1440x810
#4 = 1920x1080
factor = 4

# resolution sent to the AI model
inputRes = (480 * factor, 270 * factor)

#all prompts
endingPrompt = "Output exclusively your response to the user without any pretext. Do not use any special characters, except for common punctuation."

# 3 press prompt
initPrompt = "Your response will be read aloud to a visually-impaired user. Only speak in second-person."
descImg = initPrompt + "Describe the scene in 1 sentence. Prioritize important details." + endingPrompt
#2 press prompt 
readTxt = "Extract any text from the photo to be spoken aloud to to the user. Prices short be shortened. If you cannot reliably complete your task, output \"FAIL\" and nothing else." + endingPrompt
# 1 press prompt
descObj = "Describe the object or person towards the center of the camera. Output only one word." + endingPrompt

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
    
# gemma (the current AI model) takes image input encoded in b64
# this takes the image from the uploads folder
# and encodes it in b64
def imgToB64(imgPath):
    with open(imgPath, "rb") as img_file:
        img_data = img_file.read()

    return base64.b64encode(img_data).decode("utf-8")

#scale the ai's input image down, for resource constrained systems
# was made early on but not applicable to the laptop this was running on
# not really used here
def resizeImage(imgPath):
    img = cv2.imread(imgPath)
    img = cv2.resize(img, inputRes)
    cv2.imwrite("images/frame.png", img)

# 1 button press
# outputs only 1 word, the object in front of the camera
# dist isnt used since thats not processed on the server anymore
def describeObjectFromServer(imgPath, dist):
    b64 = imgToB64(imgPath) #encode image
    return describeImage(b64, descObj) #send image in b64 to model, along with the correct prompt

# 2 button presses
# text extraction
def extractTextFromServer(imgPath):
    b64 = imgToB64(imgPath)
    return describeImage(b64, readTxt) #same as above

# 3 button presses
# detailed description of the image
def describeImageFromServer(imgPath):
    b64 = imgToB64(imgPath)
    return describeImage(b64, descImg) # same as above