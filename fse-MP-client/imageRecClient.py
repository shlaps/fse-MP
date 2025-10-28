fileName = "captured_frame.jpg"
import os
import json
import subprocess
import imageCapture
import time

import RPi.GPIO as GPIO

buttonPin = 11

def setUp():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

setUp()

while True :
	if (GPIO.input(buttonPin)):
		fileName = imageCapture.final_img()
		result = json.loads(os.popen(f"curl -X POST -F \"image=@{fileName}\" http://192.168.68.99:5000/upload").read())
		print(result["text"], result["prompt"])
	time.sleep(0.1)
