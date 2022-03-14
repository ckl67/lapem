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

# Swap between Play and Pause
BPlayPauseSwap = 0

# Boutton Back Counter before to enter in specific mode
BBackCnt = 0
BBackCntTh= 5

# --------------------------------
# Led
# --------------------------------

# Play Led
# set GPIO18 as an output (LED)
# 5V
LEDPlay = 18

# How long we want the LED to stay on/off/time/Loop
LEDPlayONT = 1
LEDPlayOFFT = 0
LEDPlayT = -1
LEDPlayNbL = 1


# Power Led
# set GPIO17 as an output (LED)
# 5V
LEDPower = 17

# How long we want the LED to stay on/off/time/Loop
LEDPowerONT = 1
LEDPowerOFFT = 0
LEDPowerT = -1
LEDPowerNbL = 1
LEDPowerLInfinite = False

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

    global BPlayPauseSwap
    global BBackCnt
    global BBackCntTh  

    global LEDPlayONT
    global LEDPlayOFFT
    global LEDPlayNbL

    global LEDPowerNbL
    global LEDPowerOFFT
    global LEDPowerNbL
    global LEDPowerLInfinite

    if vbut == BPlayPause:

        # Swap Play Pause mode
        if BPlayPauseSwap == 0:
            BPlayPauseSwap = 1
            print("Button Play")
            LEDPlayONT = 1
            LEDPlayOFFT = 0
            LEDPlayNbL = 1

        else:
            BPlayPauseSwap = 0
            print("Button Pause")
            LEDPlayONT = 0
            LEDPlayOFFT = 1
            LEDPlayNbL = 1

        LEDPowerLInfinite = False
        BBackCnt=0  

    else:
        #Button Back Pressed
        if BBackCnt < BBackCntTh:
            print("Button Back")
            BBackCnt=BBackCnt+1  
            LEDPlayONT = 0.5
            LEDPlayOFFT = 0.5
            LEDPlayNbL = 5
        else:
            print("Spetial Mode")
            LEDPlayONT = 0.25
            LEDPlayOFFT = 0.25
            LEDPlayNbL = 20

            LEDPowerONT = 0.5
            LEDPowerOFFT = 0.5
            LEDPowerNbL = 1
            LEDPowerLInfinite = True

# ---------------------------------------------
# ---------------------------------------------
def p_LEDPlay_On():
    GPIO.output(LEDPlay, 1)

# ---------------------------------------------
# ---------------------------------------------
def p_LEDPlay_Off():
    GPIO.output(LEDPlay, 0)

# ---------------------------------------------
# ---------------------------------------------
def p_LEDPlay_Blink():

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

    # this block will run no matter how the try block exits
    except KeyboardInterrupt:
        print("Interrupt")
        GPIO.cleanup()  # clean up after yourself

