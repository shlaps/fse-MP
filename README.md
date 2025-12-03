# FSE-100: the iStick

Most of this code was written by me, with a few exceptions noted in the code.
My group members assisted with a LOT of the implementation.

This project consists of a server and a client component, both written in Python.
The code is essentially fully commentated, if you'd like to take a closer look.

## Server Directory

The server directory contains the majority of backend logic for the application. It's responsible for handling requests, processing images and sending the AI response back to the client.

### File Summary:

*   `imageRecognition.py`:  This module contains the core AI image recognition functionality. 
*   `main.py`: This file hosts the webserver and sends images uploaded to the imageRecognition module for processing.
*   `uploads/`: This directory stores uploaded images that are later processed by the server.

## Client Directory

The client directory contains the code for the raspberry Pi. This is responsible for user interaction, capturing images, and outputting the AI response.

### File Summary:

*   `imageCapture.py`: This file contains the code responsible for capturing images from a camera.
*   `Main.py`: Handles sending images and other important data to the webserver.
*   `images/`: This directory stores captured images that are sent to the server for processing.

## Button Test Directory

Experiemental fix to the button input system. Not implemented in the final design due to time constraints.

## Overall System

The client runs on a Raspberry Pi, which is connected to a camera. The client uses the `imageCapture.py` module to capture images from the camera. 
These captured images are then sent to the server using the **CLIENTS** `Main.py` file. 
The server then processes the image, using an AI model hosted on a laptop. The AI response is then sent back to the client, which the client reads aloud.
