# ========================================================
# Projet : Lapem = Lecteur Audio Pour Ecole Maternelle
# Author : Christian Klugesherz
#          christian.klugesherz@gmail.com
# Mars 2022
# ========================================================

# ========================================================
#                          Import
# ========================================================
import time
import RPi.GPIO as GPIO

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

STATE_NOTHING = 0
STATE_PLAY = 1
STATE_PAUSE = 2
STATE_BACK = 3

# --------------------------------
#  Led Index
#   Usage : LedState[STATE_PLAY][ID_PLAY]["LedMode"]
# --------------------------------

ID_PLAY = 0
ID_POWER = 1

# --------------------------------
#  Led Mode
#       For STATIC we will take the "ONT" status
#       For BLINK we will LOOP : NbL times 
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
# Led Nothing
# -------------

LedPlayNothing = {
        "LedMode"   : STATIC,
        "ONT"       : 0,
        "OFFT"      : 0,
        "NbL"       : 1
        }

LedPowerNothing = {
        "LedMode"   : STATIC, 
        "ONT"       : 1,
        "OFFT"      : 0,
        "NbL"       : 1
        }

LedNothing = [LedPlayNothing, LedPowerNothing ] 

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
        "ONT"       : 1,
        "OFFT"      : 0,
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
        "ONT"       : 1,
        "OFFT"      : 0,
        "NbL"       : 1
        }

LedPause = [LedPlayPause, LedPowerPause]

# -------------
# Led Back
# -------------
LedPlayBack = { 
        "LedMode"   : BLINK, 
        "ONT"       : 0.1,
        "OFFT"      : 0.1,
        "NbL"       : 10
        }

LedPowerBack = {
        "LedMode"   : STATIC, 
        "ONT"       : 1,
        "OFFT"      : 0,
        "NbL"       : 1
        }

LedBack = [LedPlayBack, LedPowerBack]

# --------------------------------
# LED State
#   Usage :  
#           : c_State = STATE_PAUSE
#           : if LedState[c_State][ID_PLAY]["LedMode"] == BLINK
# --------------------------------
LedState = [ LedNothing, LedPlay, LedPause, LedBack] 

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
c_State = STATE_NOTHING

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
    #print(t_LPlay)
    
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
    GPIO.add_event_detect(BUT_PLAY_PAUSE, GPIO.RISING, callback=but_callback, bouncetime=300)
    GPIO.add_event_detect(BUT_BACK, GPIO.RISING, callback=but_callback, bouncetime=300)

# ---------------------------------------------
# Button Callback fucntion
#    function which call when a signal rising edge on pin
# ---------------------------------------------
def but_callback(vbut):

    global BUTTON_BACK_THRESHOLD  

    global cnt_Bback
    global c_State 
    global c_Mode
    global sw_PlayPause

    global cnt_BlinkLedPlay
    global cnt_BlinkLedPower
    
    if vbut == BUT_PLAY_PAUSE:

        # Reinit Button Back Counter, before to enter in the Specific Mode
        cnt_Bback=0  
        
        # Reinit Blink Counters
        cnt_BlinkLedPower=0
        cnt_BlinkLedPlay=0

        # Button Play or Pause
        if sw_PlayPause == 0:
            sw_PlayPause = 1
            c_State = STATE_PLAY
            print("Button Play")
        else:
            sw_PlayPause = 0
            c_State = STATE_PAUSE
            print("Button Pause")
    else:
        #Button Back Pressed
        if cnt_Bback < BUTTON_BACK_THRESHOLD:
            print("Button Back")
            c_State = STATE_BACK
            cnt_Bback=cnt_Bback+1  
        else:
            print("Special Mode, and we stay in this Mode !!")
            c_Mode = MODE_AP

# ---------------------------------------------
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
    now = time.monotonic()

    # ------------
    # PLAY STATIC
    # ------------
    if LedState[c_State][ID_PLAY]["LedMode"] == STATIC :
        out = LedState[c_State][ID_PLAY]["ONT"]
        GPIO.output(LED_PLAY, out)

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

            if GPIO.input(LED_PLAY) == True:
                if now >= t_LPlay + onT:
                    GPIO.output(LED_PLAY, 0)
                    t_LPlay = now
                    cnt_BlinkLedPlay =  cnt_BlinkLedPlay + 1 



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
        print("Here We got an ERROR in p_LED for ID_PLAY !")


    # ------------
    # POWER STATIC
    # ------------
    if LedState[c_State][ID_POWER]["LedMode"] == STATIC :
        out = LedState[c_State][ID_POWER]["ONT"]
        GPIO.output(LED_POWER, out)

    # ------------
    # POWER BLINK
    # ------------
    elif LedState[c_State][ID_POWER]["LedMode"] == BLINK :
        onT = LedState[c_State][ID_POWER]["ONT"]
        offT = LedState[c_State][ID_POWER]["OFFT"]

        if  cnt_BlinkLedPower <= 2 * LedState[c_State][ID_POWER]["NbL"] :
            if GPIO.input(LED_POWER) == False:
                if now >= t_LPOWER + offT:
                    GPIO.output(LED_POWER, 1)
                    t_LPOWER = now
                    cnt_BlinkLedPower =  ncnt_BlinkLedPower + 1 

            if GPIO.input(LED_POWER) == True:
                if now >= t_LPOWER + onT:
                    GPIO.output(LED_POWER, 0)
                    t_LPOWER = now
                    cnt_BlinkLedPower =  ncnt_BlinkLedPower + 1 

    # ------------
    # POWER INFINITY
    # ------------
    elif LedState[c_State][ID_POWER]["LedMode"] == INFINITY :
        onT = LedState[c_State][ID_POWER]["ONT"]
        offT = LedState[c_State][ID_POWER]["OFFT"]
        if GPIO.input(LED_POWER) == False:
            if now >= t_LPOWER + offT:
                GPIO.output(LED_POWER, 1)
                t_LPOWER = now

        if GPIO.input(LED_POWER) == True:
            if now >= t_LPOWER + onT:
                GPIO.output(LED_POWER, 0)
                t_LPOWER = now

    else :
        print("Here We got an ERROR in p_LED for ID_POWER !")



# ---------------------------------------------
# ---------------------------------------------
if __name__ == '__main__':
    # call init
    
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

     # this block will run no matter how the try block exits
    except KeyboardInterrupt:
        GPIO.cleanup()  # clean up after yourself


