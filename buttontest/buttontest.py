# this file was an experimental fix to the button logic on the iStick.
# it has not been implemented due to time constraints.
# as such, comments arent as extensive as elsewhere.


import threading
import time
import os
from pygame import mixer
mixer.init()
pressSound = mixer.Sound("buttontest/beepPress.wav")
unpressSound = mixer.Sound("buttontest/beepUnpress.wav")

buttonToggle = False

# simulate how buttons work on the rasp pi
def get_input():
    global buttonToggle
    user_input = input()
    if user_input.lower() == '':
        buttonToggle = not buttonToggle
        get_input()
    elif user_input.lower() == 'exit':
        print("Exiting...")
        os._exit(0)


def main():
    # start simulation
    input_thread = threading.Thread(target=get_input, daemon=True)
    input_thread.start()

    # part of the simulation
    global buttonToggle
    lastToggle = False

    #button logic vars
    inc = 0
    buttonPress = 0

    cooldown = 0.5
    timeSinceLastPress = time.time()

    
    while True:
        # would be button pin is HIGH on the rasp pi
        # part of the rasp pi simulation, not the actual button logic
        if buttonToggle: 
            inc += 1
        #----everything after this is the actual button code----
        elif (buttonToggle != lastToggle): # on release / after 3 cooldowns
            print("Button released")
            unpressSound.play()
            inc = 0
            buttonPress = 0

        #increase buttonPress every cooldown period while held
        if (timeSinceLastPress + cooldown < time.time() and inc > 0):
            buttonPress += 1
            print("Button pressed: " + str(buttonPress))
            if buttonPress == 3:
                buttonToggle = False
                continue
            
            pressSound.play()
            timeSinceLastPress = time.time()
        lastToggle = buttonToggle
        time.sleep(0.005)

main()
