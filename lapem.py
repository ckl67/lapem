# ========================================================
# Projet : Lapem = Lecteur Audio Pour Ecole Maternelle
# Author : Christian Klugesherz
#          christian.klugesherz@gmail.com
# Mars 2022
#
#   To run at the start : /etc/rc.local
#   add before exit 0
#       /usr/bin/python3 /home/pi/lapem/lapem.py &
# ========================================================

# ========================================================
#                          Import
# ========================================================

from time import sleep, monotonic
from common import setApplicationDebugLevel, pError, pDbg0, pDbg1, pDbg2

import RPi.GPIO as GPIO
import subprocess
import os
import json

from pygame import mixer # sudo apt-get install python3-pygame

# ========================================================
#                       Declarations
# ========================================================

# --------------------------------
# DEBUG_LEVEL
# --------------------------------
DEBUG_LEVEL = 0

# --------------------------------
# Lapem Mode
#   MODE_AP     : Access Point
#   MODE_CLIENT : Wifi Client
# --------------------------------

MODE_AP = 0
MODE_CLIENT = 1

# --------------------------------
# Will check every 20 seconds the Mode Status
# --------------------------------

LOOP_MODE_TIME = 20

# --------------------------------
# Button
# --------------------------------
# Play-Pause Button
# set GPIO25 as input (button)
# Internal Pull Down to avoid external resistors
# 3,3 V
BUT_PLAY_PAUSE = 25

# Back Button
# set GPIO24 as input (button)
# Internal Pull Down to avoid external resistors
# 3,3 V
BUT_BACK = 24

# --------------------------------
# Threshold before to access to Specific Mode
# --------------------------------
BUTTON_BACK_THRESHOLD= 5

# --------------------------------
# Led
# --------------------------------

# Play Led
# set GPIO18 as an output (LED)
# 5V
LED_PLAY = 18

# Power Led
# set GPIO17 as an output (LED)
# 5V
LED_POWER = 17

# --------------------------------
#   Index for LedState
#   Usage : LedState[STATE_PLAY][ID_PLAY]["LedMode"]
# --------------------------------

STATE_STOP = 0
STATE_PLAY = 1
STATE_PAUSE = 2

# --------------------------------
#  Led Index
#   Usage : LedState[STATE_PLAY][ID_PLAY]["LedMode"]
# --------------------------------

ID_PLAY = 0
ID_POWER = 1

# --------------------------------
#  Led Mode
#       For STATIC we will take the "ONT" status > 0 --> 1
#           Take care to think to programm the Good value for Blink and Infinity
#       For BLINK we will Loop with the ONT & OFFT NbL times, and we will end with a 0
#       For INFINITY we will Loop with the ONT & OFFT infinity
#
#   Usage : LedState[STATE_PLAY][ID_PLAY]["LedMode"] = BLINK
#
# --------------------------------

STATIC = 0
BLINK = 1
INFINITY = 2

# ========================================================
#                      Variables LED
# ========================================================
# -------------
# Led Stop
# -------------

LedPlayStop = {
        "LedMode"   : BLINK,
        "ONT"       : 0.08,
        "OFFT"      : 0.08,
        "NbL"       : 4
        }

LedPowerStop = {
        "LedMode"   : STATIC,
        "ONT"       : 0.5,
        "OFFT"      : 0.5,
        "NbL"       : 1
        }

LedStop = [LedPlayStop, LedPowerStop ]

# -------------
# Led Play
# -------------

LedPlayPlay = {
        "LedMode"   : STATIC,
        "ONT"       : 1,
        "OFFT"      : 0,
        "NbL"       : 1,
        }

LedPowerPlay = {
        "LedMode"   : STATIC,
        "ONT"       : 0.5,
        "OFFT"      : 0.5,
        "NbL"       : 1,
        }

LedPlay = [LedPlayPlay, LedPowerPlay]

# -------------
# Led Pause
# -------------
LedPlayPause = {
        "LedMode"   : STATIC,
        "ONT"       : 0,
        "OFFT"      : 0,
        "NbL"       : 1
        }

LedPowerPause = {
        "LedMode"   : STATIC,
        "ONT"       : 0.5,
        "OFFT"      : 0.5,
        "NbL"       : 1
        }

LedPause = [LedPlayPause, LedPowerPause]

# --------------------------------
# LED State
#   Usage :
#           : c_State = STATE_PAUSE
#           : if LedState[c_State][ID_PLAY]["LedMode"] == BLINK
# --------------------------------
LedState = [ LedStop, LedPlay, LedPause]

# ========================================================
#                       Variables
# ========================================================
# General Timer
now = 0

# Swicht between Play and Pause
sw_PlayPause = 0

# Led Power timer
t_LPower = -1

# Led Play timer
t_LPlay = -1

# Current Lapem Mode
c_Mode = MODE_AP

# Timer Mode
t_Mode = 0

# Current Lapem Led State
c_State = STATE_STOP

# Blink Counter for Led Play
cnt_BlinkLedPlay = 0

# Blink Counter for Led Power
cnt_BlinkLedPower = 0

# Audio level
v_audio_level = 1
# ========================================================
#                         Functions
# ========================================================
# ---------------------------------------------
# init function
#     All your initialization here
# ---------------------------------------------
def init():

    # Input declaration Mode : BCM GPIO numbering
    GPIO.setmode(GPIO.BCM)

    # Leds
    GPIO.setup(LED_PLAY, GPIO.OUT)
    GPIO.setup(LED_POWER, GPIO.OUT)

    # Default status
    GPIO.output(LED_PLAY, 0)
    GPIO.output(LED_POWER, 1)

    # Button
    GPIO.setup(BUT_PLAY_PAUSE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(BUT_BACK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Add an interrupt on pin on rising edge
    GPIO.add_event_detect(BUT_PLAY_PAUSE, GPIO.RISING, callback=state_machine, bouncetime=300)
    GPIO.add_event_detect(BUT_BACK, GPIO.RISING, callback=state_machine, bouncetime=300)

    # Read Audio level
    read_volume()

    exit()

    mixer.init() #Initialzing pyamge mixer

    #Loading Music File
    mixer.music.load('/home/pi/lapem/music/audio.wav')
    mixer.music.set_volume(v_audio_level)
    mixer.music.play()  #Playing Music with Pygame
    mixer.music.pause() #pausing music file

# ---------------------------------------------
# Read Volume in file : volume.txt
# ---------------------------------------------
def read_volume():
    string1 = 'Volume'
  
    # opening a text file
    file1 = open("volume.txt", "r")
  
    # setting flag and index to 0
    flag = 0

    # Loop through the file line by line
    for line in file1:    
        # checking string is present in line or not
        if string1 in line:
            flag = 1
            break 
          
    # checking condition for string found or not
    if flag == 0: 
        pError('String', string1 , 'Not Found') 
    else: 
        #pDbg0("Line : {}".format(line))
        res = ""

        for possibility in line.split():
            try:
                res = str(float(possibility.replace(',', '.')))
            except ValueError:
                pass
        print(res)
        
    # closing text file    
    file1.close() 

# ---------------------------------------------
# Button Callback function
#    function which call when a signal rising edge on pin
#    This will set the current state and current mode
# ---------------------------------------------
def state_machine(vbut):

    global c_State
    global c_Mode
    global sw_PlayPause

    global cnt_BlinkLedPlay
    global cnt_BlinkLedPower

    global v_audio_level

    # Reinit Blink Counters
    cnt_BlinkLedPower=0
    cnt_BlinkLedPlay=0

    if vbut == BUT_PLAY_PAUSE:

        # Button Play or Pause
        if sw_PlayPause == 0:
            sw_PlayPause = 1
            c_State = STATE_PLAY
            pDbg1("State Play")
            mixer.music.unpause() #unpausing music file

        else:
            sw_PlayPause = 0
            c_State = STATE_PAUSE
            pDbg1("State Pause")
            mixer.music.pause() #pausing music file

    else: #Button Back Pressed
        # Force Button Play/Pause as Pause
        sw_PlayPause = 0

        pDbg1("State Stop")
        c_State = STATE_STOP
        mixer.music.stop()
        mixer.music.load('/home/pi/lapem/music/audio.wav')
        mixer.music.set_volume(v_audio_level)
        mixer.music.play()  #Playing Music with Pygame
        mixer.music.pause() #pausing music file

# ---------------------------------------------
#  Check Mode change every 10 secondes
# ---------------------------------------------
def p_Mode():
    global t_Mode
    global c_Mode

    ip_address = ""

    if now >= t_Mode + LOOP_MODE_TIME:

        t_Mode = now

        # Get IP Address of wan0
        routes = json.loads(os.popen("ip -j -4 route").read())
        for r in routes:
            if r.get("dev") == "wlan0" and r.get("prefsrc"):
                ip_address = r["prefsrc"] 
                continue
        pDbg2("IP: {}".format(ip_address))

        if ip_address == "10.3.141.1":
            c_Mode = MODE_AP
        else:
            c_Mode = MODE_CLIENT

        if c_Mode == MODE_AP :
            LedState[c_State][ID_POWER]["LedMode"] = STATIC
            pDbg1("AP Mode : IP = {}".format(ip_address))

        else:
            # c_Mode = MODE_CLIENT
            LedState[c_State][ID_POWER]["LedMode"] = INFINITY
            pDbg1("Client Mode : IP = {}".format(ip_address))

# ---------------------------------------------
#
# ---------------------------------------------
def p_LED():

    # Clarifications
    # If you set a value of a variable inside the function, python understands it as creating a local variable with that name.
    # This local variable masks the global variable.

    global t_LPlay
    global t_LPower

    global cnt_BlinkLedPlay
    global cnt_BlinkLedPower

    # ------------
    # PLAY STATIC
    # ------------
    if LedState[c_State][ID_PLAY]["LedMode"] == STATIC :
        out = LedState[c_State][ID_PLAY]["ONT"]
        if out > 0 :
            GPIO.output(LED_PLAY, 1)
        else:
            GPIO.output(LED_PLAY, 0)

    # ------------
    # PLAY BLINK
    # ------------
    elif LedState[c_State][ID_PLAY]["LedMode"] == BLINK :
        onT = LedState[c_State][ID_PLAY]["ONT"]
        offT = LedState[c_State][ID_PLAY]["OFFT"]

        if  cnt_BlinkLedPlay < 2 * LedState[c_State][ID_PLAY]["NbL"] :

            if GPIO.input(LED_PLAY) == False:
                if now >= t_LPlay + offT:
                    GPIO.output(LED_PLAY, 1)
                    t_LPlay = now
                    cnt_BlinkLedPlay =  cnt_BlinkLedPlay + 1
                    #pDbg1(cnt_BlinkLedPlay )

            if GPIO.input(LED_PLAY) == True:
                if now >= t_LPlay + onT:
                    GPIO.output(LED_PLAY, 0)
                    t_LPlay = now
                    cnt_BlinkLedPlay =  cnt_BlinkLedPlay + 1
                    #pDbg1(cnt_BlinkLedPlay )
        else : # For BLINK, we will stop with LED Turn Off
            GPIO.output(LED_PLAY, 0)

    # ------------
    # PLAY INFINITY
    # ------------
    elif LedState[c_State][ID_PLAY]["LedMode"] == INFINITY :
        onT = LedState[c_State][ID_PLAY]["ONT"]
        offT = LedState[c_State][ID_PLAY]["OFFT"]
        if GPIO.input(LED_PLAY) == False:
            if now >= t_LPlay + offT:
                GPIO.output(LED_PLAY, 1)
                t_LPlay = now

        if GPIO.input(LED_PLAY) == True:
            if now >= t_LPlay + onT:
                GPIO.output(LED_PLAY, 0)
                t_LPlay = now

    else :
        pError("Here We got an ERROR in p_LED for ID_PLAY !")
        pError("(p_LED) c_State= {}".format(c_State))
        pError("(p_LED) Led State= {}".format(LedState[c_State][ID_PLAY]["LedMode"]))

    # ------------
    # POWER STATIC
    # ------------
    if LedState[c_State][ID_POWER]["LedMode"] == STATIC :
        out = LedState[c_State][ID_POWER]["ONT"]
        if out > 0 :
            GPIO.output(LED_POWER, 1)
        else:
            GPIO.output(LED_POWER, 0)

    # ------------
    # POWER BLINK
    # ------------
    elif LedState[c_State][ID_POWER]["LedMode"] == BLINK :
        onT = LedState[c_State][ID_POWER]["ONT"]
        offT = LedState[c_State][ID_POWER]["OFFT"]

        if  cnt_BlinkLedPower <= 2 * LedState[c_State][ID_POWER]["NbL"] :
            if GPIO.input(LED_POWER) == False:
                if now >= t_LPower + offT:
                    GPIO.output(LED_POWER, 1)
                    t_LPower = now
                    cnt_BlinkLedPower =  cnt_BlinkLedPower + 1

            if GPIO.input(LED_POWER) == True:
                if now >= t_LPower + onT:
                    GPIO.output(LED_POWER, 0)
                    t_LPower = now
                    cnt_BlinkLedPower =  cnt_BlinkLedPower + 1

        else : # For BLINK, we will stop with LED Turn Off
            GPIO.output(LED_POWER, 0)

    # ------------
    # POWER INFINITY
    # ------------
    elif LedState[c_State][ID_POWER]["LedMode"] == INFINITY :
        onT = LedState[c_State][ID_POWER]["ONT"]
        offT = LedState[c_State][ID_POWER]["OFFT"]
        if GPIO.input(LED_POWER) == False:
            if now >= t_LPower + offT:
                GPIO.output(LED_POWER, 1)
                t_LPower = now

        if GPIO.input(LED_POWER) == True:
            if now >= t_LPower + onT:
                GPIO.output(LED_POWER, 0)
                t_LPower = now

    else :
        pError("Here We got an ERROR in p_LED for ID_POWER !")
        pError("(p_LED) c_State= {}".format(c_State))
        pError("(p_LED) Led State= {}".format(LedState[c_State][ID_POWER]["LedMode"]))

# ---------------------------------------------
# ---------------------------------------------
if __name__ == '__main__':
    # call init

    setApplicationDebugLevel(DEBUG_LEVEL )

    init()

    try:
        # looping infinitely
        while True:

            # monotonic only available in Python3 !
            now = monotonic()

            p_Mode()

            p_LED()

            sleep(0.1)

     # this block will run no matter how the try block exits
    except KeyboardInterrupt:
        GPIO.cleanup()  # clean up after yourself


