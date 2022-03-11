import time
import RPi.GPIO as GPIO

flag_callback = False

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

# Play Led
# set GPIO18 as an output (LED)
# 5V
LEDPlay = 18

# How long we want the LED to stay on/off/time
BPlayONT = 0.5
BPlayOFFT = 0.25
BPlayBT = -1

BBackONT = 1
BBackOFFT = 0
BBackBT = -1

# Power Led
# set GPIO17 as an output (LED)
# 5V
LEDPower = 17


def init():
    # make all your initialization here
    # Input declaration Mode : BCM GPIO numbering
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(LEDPlay, GPIO.OUT)
    GPIO.setup(LEDPower, GPIO.OUT)

    # Init Leds
    GPIO.output(LEDPlay, 0)
    GPIO.output(LEDPower, 1)

    # Button
    GPIO.setup(BPlayPause, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(BBack, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # add an interrupt on pin on rising edge
    GPIO.add_event_detect(BPlayPause, GPIO.RISING, callback=my_callback, bouncetime=300)
    GPIO.add_event_detect(BBack, GPIO.RISING, callback=my_callback, bouncetime=300)

def my_callback(vbut):
    # callback = function which call when a signal rising edge on pin
    global flag_callback
    global BPlayONT
    global BPlayOFFT
    global BBackONT
    global BBackOFFT
    
    flag_callback = True
    print(vbut)

    if vbut == BPlayPause:
        print("Button Play Pause")
        BPlayONT = 1
        BPlayOFFT = 0
    elif vbut == BBack:
        BBackONT = 0.5
        BBackOFFT = 0.5
    else:
        print("Button Back")
        BPlayONT = 0
        BPlayOFFT = 0

def process_callback():
    # make process here
    print('something')

if __name__ == '__main__':
    # your main function here
    try:
        # 1- first call init function
        init()

        # 2- looping infinitely
        while True:
            #3- test if a callback happen

            now = time.monotonic()


            if GPIO.input(LEDPlay) == False:
                if now >= BPlayBT + BPlayOFFT:
                    GPIO.output(LEDPlay, 1)
                    BPlayBT = now
            if GPIO.input(LEDPlay) == True:
                if now >= BPlayBT + BPlayONT:
                    GPIO.output(LEDPlay, 0)
                    BPlayBT = now


            if GPIO.input(LEDPower) == False:
                if now >= BBackBT + BBackOFFT:
                    GPIO.output(LEDPower, 1)
                    BBackBT = now
            if GPIO.input(LEDPower) == True:
                if now >= BBackBT + BBackONT:
                    GPIO.output(LEDPower, 0)
                    BBackBT = now



            if flag_callback :
                #4- call a particular function
                process_callback()
                #5- reset flag for next interrupt
                flag_callback = False
        pass

    # this block will run no matter how the try block exits
    finally:
        GPIO.cleanup()  # clean up after yourself


