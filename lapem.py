# ========================================================
# Projet Lapem : Lecteur Audio Pour Ecole Maternelle
# Christian Klugesherz
# christian.klugesherz@gmail.com
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
# Button
# --------------------------------
# Play-Pause Button
# set GPIO25 as input (button)
# Internal Pull Down to avoid external resistors
# 3,3 V
BPlayPause = 25

# Back Button
# set GPIO24 as input (button)
# Internal Pull Down to avoid external resistors
# 3,3 V
BBack = 24

# --------------------------------
# Led
# --------------------------------

# Play Led
# set GPIO18 as an output (LED)
# 5V
LEDPlay = 18

# Power Led
# set GPIO17 as an output (LED)
# 5V
LEDPower = 17

# -------------
# Led Nothing
# -------------
# Mode : "Static", "Blinck", "Infinity"
# For Static we will take the "ONT" status
# For Dynamic we will end by OFFT
LedPlayNothing = { 
        "Mode"   : "Static", 
        "ONT"    : 0,
        "OFFT"   : 0,
        "NbL"    : 1
        }

LedPowerNothing = {
        "Mode"   : "Static", 
        "ONT"    : 1,
        "OFFT"   : 0,
        "NbL"    : 1
        }

LedNothing = [LedPlayNothing, LedPowerNothing]

# -------------
# Led Play
# -------------
# Mode : "Static", "Blinck", "Infinity"
# For Static we will take the "ONT" status
# For Dynamic we will end by OFFT
LedPlayPlay = { 
        "Mode"   : "Static", 
        "ONT"    : 1,
        "OFFT"   : 0,
        "NbL"    : 1
        }
LedPowerPlay = {
        "Mode"   : "Static", 
        "ONT"    : 1,
        "OFFT"   : 0,
        "NbL"    : 1
        }

LedPlay = [LedPlayPlay, LedPowerPlay]

# -------------
# Led Pause
# -------------
# Mode : "Static", "Blinck", "Infinity"
# For Static we will take the "ONT" status
# For Dynamic we will end by OFFT
LedPlayPause = { 
        "Mode"   : "Static", 
        "ONT"    : 0,
        "OFFT"   : 0,
        "NbL"    : 5
        }

LedPowerPause = {
        "Mode"   : "Static", 
        "ONT"    : 1,
        "OFFT"   : 0,
        "NbL"    : 1
        }

LedPause = [LedPlayPause, LedPowerPause]

# -------------
# Led Back
# -------------
# Mode : "Static", "Blinck", "Infinity"
# For Static we will take the "ONT" status
# For Dynamic we will end by OFFT
LedPlayBack = { 
        "Mode"   : "Blink", 
        "ONT"    : 0.5,
        "OFFT"   : 0.5,
        "NbL"    : 3
        }

LedPowerBack = {
        "Mode"   : "Static", 
        "ONT"    : 1,
        "OFFT"   : 0,
        "NbL"    : 1
        }

LedBack = [LedPlayBack, LedPowerBack]

# --------------------------------
# Lapem Led State 
# Nothing
# --------------------------------
LapemLedState = { 
        'Nothing'   : LedNothing,
        'Play'      : LedPlay,
        'Pause'     : LedPause,
        'Back'      : LedBack, 
        }

print(LapemMode[cState][ID_LED_POWER]["Mode"])

# --------------------------------
# Lapem Mode 
#   AP: Access Point
#   WC: Wifi Client
# --------------------------------
LapemMode = { 
        'Mode'   : "AP",
        }


# --------------------------------
# --------------------------------
BBackCntTh= 5

# ========================================================
#                       Variables
# ========================================================

# Swap between Play and Pause
swapPlayPauseMode = 0

# Boutton Back Counter before to enter in specific mode
cntBBack = 0

# Led Power timer
tLEDPower = -1

# Led Play timer
tLEDPlay = -1

# Current Lapem Mode
cLapemMode = "AP" 

# Current Lapem Led State
cLapemLedState = "Noting"

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
    GPIO.setup(LEDPlay, GPIO.OUT)
    GPIO.setup(LEDPower, GPIO.OUT)

    GPIO.output(LEDPlay, 0)
    GPIO.output(LEDPower, 1)

    # Button
    # add an interrupt on pin on rising edge
    GPIO.setup(BPlayPause, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(BBack, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(BPlayPause, GPIO.RISING, callback=but_callback, bouncetime=300)
    GPIO.add_event_detect(BBack, GPIO.RISING, callback=but_callback, bouncetime=300)

# ---------------------------------------------
# button Callback fucntion
#    function which call when a signal rising edge on pin
# ---------------------------------------------
def but_callback(vbut):

    global BBackCntTh  
    global cntBBack
    
    global cLapemLedState 
    global cLapemMode
    
    global swapBPlayPause

    if vbut == BPlayPause:

        cntBBack=0  
        # Swap Play Pause mode
        if swapBPlayPause == 0:
            swapBPlayPause = 1
            cLapemLedState = "Play"
            print("Button Play")
        else:
            swapBPlayPause = 0
            cLapemLedState = "Pause"
            print("Button Pause")
    else:
        #Button Back Pressed
        if cntBBack < BBackCntTh:
            print("Button Back")
            cLapemLedState = "Back"
            cntBBack=cntBBack+1  
        else:
            print("Special Mode")
            cLapemMode = "AP"

# ---------------------------------------------
# ---------------------------------------------
def p_LED_Blink():

    # monotonic only available in Python3 !
    now = time.monotonic()

    if LEDPlayNbL > 0:
        if GPIO.input(LEDPlay) == False:
            if now >= LEDPlayT + LEDPlayOFFT:
                GPIO.output(LEDPlay, 1)
                LEDPlayT = now
                LEDPlayNbL =  LEDPlayNbL - 1 
        if GPIO.input(LEDPlay) == True:
            if now >= LEDPlayT + LEDPlayONT:
                GPIO.output(LEDPlay, 0)
                LEDPlayT = now
                LEDPlayNbL =  LEDPlayNbL - 1 

# ---------------------------------------------
# ---------------------------------------------
def p_LEDPower_Blink():
    
    # monotonic only available in Python3 !
    now = time.monotonic()
    if LEDPowerNbL > 0 or LEDPowerLInfinite == True : 
        if GPIO.input(LEDPower) == False:
            if now >= LEDPowerT + LEDPowerOFFT:
                GPIO.output(LEDPower, 1)
                LEDPowerT = now
                LEDPowerNbL = LEDPowerNbL - 1

        if GPIO.input(LEDPower) == True:
            if now >= LEDPowerT + LEDPowerONT:
                GPIO.output(LEDPower, 0)
                LEDPowerT = now
                LEDPowerNbL = LEDPowerNbL - 1

# ---------------------------------------------
# ---------------------------------------------
def p_LEDPower_On():
    GPIO.output(LEDPower, 1)

# ---------------------------------------------
# ---------------------------------------------
def p_LEDPower_Off():
    GPIO.output(LEDPower, 0)


# ---------------------------------------------
# ---------------------------------------------
def process_callback():
    # make process here
    print('something')


# ---------------------------------------------
# ---------------------------------------------
if __name__ == '__main__':
    # call init
    init()

    try:
        # looping infinitely
        while True:
            p_LEDPlay_On()

     # this block will run no matter how the try block exits
    except KeyboardInterrupt:
        print("Interrupt")
        GPIO.cleanup()  # clean up after yourself

