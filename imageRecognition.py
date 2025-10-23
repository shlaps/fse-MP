from ollama import generate

import warnings
import base64
import os
import cv2

llmModel = "gemma3:12b"
path = "images" # path to the images to describe
paths = []  # path to each individual image from prj root

for img in os.listdir(path):
   paths.append(path + "/" + img)

#code block modified from https://github.com/ollama/ollama-python/issues/283 user: pnmartinez
for x, img_path in enumerate(paths):
  try:
    # Read the image file as binary data
    with open(img_path, 'rb') as img_file:
        img_data = img_file.read()
    
    # Convert image to base64 for Ollama
    img_base64 = base64.b64encode(img_data).decode('utf-8')


    response = generate(
        model=llmModel,
        prompt="Your response will be read aloud to a visually-impaired user. Describe the image captured from the device provided to the user. Warn the user of any imminent obstacles or danger first. Summarize text as you see fit. Keep your response brief, unless the image shown displays lengthy text you feel may need to be read-aloud in more depth. Output exclusively your response to the user without any pretext. Do not use any special characters.",
        images=[img_base64],  # Pass base64 encoded image data at top level
        options={"temperature": 0.1}  # "imagination" of the ai response
    )

    caption = response['response'].strip()
    print(str(x + 1) + ": " + caption + "\n\n")
  except:
    warnings.warn("Failed opening " + img_path)