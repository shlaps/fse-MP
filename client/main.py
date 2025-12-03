# THIS FILE IS RUN ON THE PI
# this file sends over camera data for processing on the webserver
# to see the webserver code, go to server/main.py

#libraries
import os
import time
import RPi.GPIO as GPIO

#handles communication wit the webserver
import requests

#!!! this is a custom python module that handles image capture !!!
# you can see the code by navigating to client/imageCapture.py
import imageCapture

#input button
buttonPin = 11
# haptic buzzer
buzzerPin = 13

#pins for ultrasonic sensor
trigPin = 29 #GPIO 5
echoPin = 31 # GPIO 6

#DEPRECIATED: was for improving accuracy of echo sensor
loopCount = 3

#image to send to server
imgPath = "images/flipped.jpg"

# server URL
serverURL = "http://192.168.68.99:5000/upload"

print("running!")

#get ultrasonic sensor data
# taken from one of the example programs earlier -
# - in the year
def distance():
	GPIO.output(trigPin, 0)
	time.sleep(0.000002)

	GPIO.output(trigPin, 1)
	time.sleep(0.00001)
	GPIO.output(trigPin, 0)

	
	while GPIO.input(echoPin) == 0:
		a = 0
	time1 = time.time() 
	while GPIO.input(echoPin) == 1:
		a = 1	
	time2 = time.time()

	during = time2 - time1
	return int(during * 340 / 2 * 100) #CM

# setup the pins for buzzer, button and ultrasonic sensor in that order
def setUp():
	#ensure setup pins are for the correct pin #'s
	GPIO.setmode(GPIO.BOARD)
	#buzzer pin
	GPIO.setup(buzzerPin, GPIO.OUT)
	#button pin
	GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	
	# ultrasonic sensor pins
	GPIO.setup(trigPin, GPIO.OUT)
	GPIO.setup(echoPin, GPIO.IN)

# buzz haptic sensor for .3 seconds
def notifyUser():
	GPIO.output(buzzerPin, GPIO.HIGH)
	time.sleep(0.3)
	GPIO.output(buzzerPin, GPIO.LOW)
	
# get image from file as byte array
# this data is sent raw over to the server
# could probably be compressed for better performance
def openImg(imgPath):
    with open(imgPath, "rb") as img_file:
        img_data = img_file.read()

    return img_data

# TODO: OUTDATED FUNCTION
# on the pi's code, this actually just divides -
# - the cm by a value and returns that as the step count
# I also believe I removed this function and moved it to getDistOutput()
def findDistStr(cm):
	diffArm = cm - 70 # 1 step
	diffNear = cm - 100 # near
	print(cm)
	res = 7
	
	if (diffArm <= res):
		return "one step away"
	elif (diffNear <= res):
		return "near"
	else:
		return "far away"
		
#TODO: OUTDATED FUNCTION
def getDistOutput(resp):
	dist = distance()
	distStr = findDistStr(dist)
	
	return f"The {resp} is {distStr}."
    
# DEPRECIATED: Used to be used to improve ultrasonic sensor accuracy. was deemed unnessesary
def getUltraSonicSensord():
	total = 0
	for x in range(loopCount):
		total += distance()
		time.sleep(0.005)
	total /= loopCount
	return int(total)

# send request to server with image and prompt number
def sendRequest(promptNum):
	# take photo. the image is stored on the pi in the images folder.
	imageCapture.takePhoto()
	# image data to send to the server
	files = {'image': openImg(imgPath)}
	# different things the server needs to know, like the prompt number and image format. 
	# because of how the requests library sends data over, the server wont know the file format. we send that over here as well
	headers = {'prompt': f"{promptNum}", "imgFormat": imgPath.split(".")[1]}
	# this is actually unused in the code, but I'm keeping it here to show - 
	# - that we can send other types of data over to the server as well
	if (promptNum == 1):
		headers["dist"] = str(distance())
	
	# send the request to the server and get the response. 
	result = requests.post(url=serverURL, files=files, headers=headers).json()["text"]
	
	# the AI is prompted to only output one word in prompt 1.
	# this function formats the AI response to also include how many steps away the object is from the user.
	if (promptNum == 1):
		return getDistOutput(result)
	
	# return the AI response
	return result

# ---- very, very overcomplicated button stuff ----
# inaccurate and hard to read.
# to see a better system (unimplemented) - 
# - go to buttontest/buttontest.py

pressCount = 0
timeSinceLastPress = time.time()
cooldown = .5

canPressCooldown = .5
timeSinceLastCooldown = time.time()
canPress = True

startPress = False

# takes how many times the button isnt pressed in .5 seconds and -
# - translates it into the prompt number
# this is where a lot of the finicky-ness of the input system is from
def findPressCount(pressCount):
	diff40 = abs(pressCount - 40) # 1 press
	diff30 = abs(pressCount - 30) # 2 presses
	diff20 = abs(pressCount - 20) # 3 presses
	
	res = 7
	
	if (diff40 <= res):
		return 1
	elif (diff30 <= res):
		return 2
	elif (diff20 <= res):
		return 3

# setup the pins before running the main program
setUp()

# having an unbroken loop like below is usually pretty bad practice -
# - but we never changed it haha

# most of this is button logic
# it's a bit of a mess
while True :
	isPressed = GPIO.input(buttonPin) #read button state
	
	#make sure the button press doesn't rapidly increase
	canPress = (timeSinceLastCooldown + canPressCooldown <= time.time())
	
	if (canPress and pressCount == 0 and isPressed and timeSinceLastPress + cooldown <= time.time()): #start press
		timeSinceLastPress = time.time()
		startPress = True
	elif (startPress and isPressed == 0): #counts how many times the button is NOT pressed
		pressCount += 1
	
	if (timeSinceLastPress + cooldown <= time.time() and pressCount != 0): #end press
		# here we actually send the image over to the webserver
		try:
			# get the number of presses and send it to the server
			buttonPress = findPressCount(pressCount) 
			# send request
			txt = sendRequest(buttonPress)
			#print for debug
			print(txt) 
			# read text aloud and buzz the haptic buzzer
			os.popen(f"espeak \"{txt}\" -s 120")
			notifyUser() 
		except:
			# mostly so the client doesnt crash on a server error
			print("failed upload")
		# more button stuff
		timeSinceLastCooldown = time.time()
		pressCount = 0
		startPress = False
	# so theres no instruction overflow
	time.sleep(0.01)
	
# this is best practice but are never actually called -
# - since the while loop above is never exited
# whoopsies
GPIO.cleanUp()
imageCapture.exit() 
