# ========================================================
# Projet : Lapem = Lecteur Audio Pour Ecole Maternelle
# Author : Christian Klugesherz
#          christian.klugesherz@gmail.com
# Mars 2022
# ========================================================

# ========================================================
#                          Import
# ========================================================

from pygame import mixer # sudo apt-get install python3-pygame

from time import sleep, monotonic
import RPi.GPIO as GPIO
from common import setApplicationDebugLevel, pError, pDbg0, pDbg1, pDbg2  

# ========================================================
#                       Declarations
# ========================================================

# --------------------------------
# Lapem Mode 
#   MODE_AP     : Access Point
#   MODE_CLIENT : Wifi Client
# --------------------------------

MODE_AP = 0
MODE_CLIENT = 1

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

# Swicht between Play and Pause
sw_PlayPause = 0

# Button Back Counter before to enter in a Specific Mode
cnt_Bback = 0

# Led Power timer
t_LPower = -1

# Led Play timer
t_LPlay = -1

# Current Lapem Mode
c_Mode = MODE_AP

# Current Lapem Led State
c_State = STATE_STOP

# Blink Counter for Led Play
cnt_BlinkLedPlay = 0

# Blink Counter for Led Power
cnt_BlinkLedPower = 0

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

    mixer.init() #Initialzing pyamge mixer

    #Loading Music File
    mixer.music.load('/home/pi/lapem/music/audio.mp3') 
    mixer.music.play()  #Playing Music with Pygame
    mixer.music.pause() #pausing music file

# ---------------------------------------------
# Button Callback function
#    function which call when a signal rising edge on pin
#    This will set the current state and current mode
# ---------------------------------------------
def state_machine(vbut):

    global BUTTON_BACK_THRESHOLD  

    global cnt_Bback
    global c_State 
    global c_Mode
    global sw_PlayPause

    global cnt_BlinkLedPlay
    global cnt_BlinkLedPower
    
    # Reinit Blink Counters
    cnt_BlinkLedPower=0
    cnt_BlinkLedPlay=0
    
    if vbut == BUT_PLAY_PAUSE:

        # Reinit Button Back Counter, before to enter in the Specific Mode
        cnt_Bback=0  

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

        if cnt_Bback < BUTTON_BACK_THRESHOLD:
            pDbg1("State Stop")
            c_State = STATE_STOP
            mixer.music.stop()
            mixer.music.load('/home/pi/lapem/music/audio.mp3') 
            mixer.music.play()  #Playing Music with Pygame
            mixer.music.pause() #pausing music file

            cnt_Bback=cnt_Bback+1  
        else:
            pDbg1("Special Mode, and we stay in this Mode !!")
            c_Mode = MODE_CLIENT

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

    # monotonic only available in Python3 !
    now = monotonic()

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

    setApplicationDebugLevel(2)
 
    init()

    try:
        # looping infinitely
        while True:

            if c_Mode == MODE_AP :
                LedState[c_State][ID_POWER]["LedMode"] = STATIC
            else:
                # c_Mode = MODE_CLIENT
                LedState[c_State][ID_POWER]["LedMode"] = INFINITY
            
            p_LED()

        sleep(0.1)

     # this block will run no matter how the try block exits
    except KeyboardInterrupt:
        GPIO.cleanup()  # clean up after yourself


