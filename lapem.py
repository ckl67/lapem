# ------------------------------------------------------
# Program : LAPEM Lecteur Audio Pour Ecole Marternelle
# Copyright : Christian Klugesherz 2022
# ------------------------------------------------------

# ==========================================================
# pygame used to plau audio
from pygame import mixer

#Initialzing pyamge mixer
mixer.init() 

# GPIO
import RPi.GPIO as GPIO

# Time
from time import sleep

# To run OS commands
import subprocess

# ========================================================


#subprocess.call(['sudo', 'ls', '-l'])
#subprocess.call(['sudo', 'service', 'lighttpd' , 'start'])
#sleep(1)
#subprocess.call(['sudo', 'ifconfig', 'wlan0'])
#exit

# Input declaration Mode : BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Play-Pause Button
# set GPIO25 as input (button)
# Internal Pull Down to avoid external resistors
# 3,3 V
BPlayPause = 25
GPIO.setup(BPlayPause, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Back Button
# set GPIO24 as input (button)
# Internal Pull Down to avoid external resistors
# 3,3 V
BBack = 24
GPIO.setup(BBack, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Play Led
# set GPIO18 as an output (LED)
# 5V
LEDPlay = 18
GPIO.setup(LEDPlay, GPIO.OUT)
# PWM at Frequncy 1
#GPIO.PWM(LEDPlay, 50)

# Power Led
# set GPIO17 as an output (LED)
# 5V
LEDPower = 17
GPIO.setup(LEDPower, GPIO.OUT)


# Inti Leds
GPIO.output(LEDPlay, 0)
GPIO.output(LEDPower, 1)


# Functionnal Variable
CurrentButtonPlayPause = 0  # 1=Play 0=Pause
ToggleButtonPlayPause = 0
oneshot = 0

# Specif mode Lan
SwitchToLanCntMax = 5
SwitchToLanCnt = 0

# Audio
#Loading Music File
mixer.music.load('/home/pi/lapem/music/audio.mp3')
mixer.music.play()  #Playing Music with Pygame
mixer.music.pause() #pausing music file


try:
    while True: # this will carry on until you hit CTRL+C
        if GPIO.input(BPlayPause):
            SwitchToLanCnt = 0
            if CurrentButtonPlayPause == 0 :
                if oneshot == 0:
                    print "Play"
                    oneshot = 1
                    GPIO.output(LEDPlay, 1)
                    ToggleButtonPlayPause = 1
                    mixer.music.unpause()
            else:
                if oneshot == 0:
                    print "Pause"
                    oneshot = 1
                    GPIO.output(LEDPlay, 0)
                    ToggleButtonPlayPause = 0
                    mixer.music.pause()

        elif GPIO.input(BBack):
            if oneshot == 0 :
                SwitchToLanCnt = SwitchToLanCnt + 1

                if SwitchToLanCnt < SwitchToLanCntMax :
                    print "Button Back is pressed will Stop also"
	            oneshot = 1
                    ToggleButtonPlayPause = 0
                    mixer.music.stop()
                    mixer.music.load('/home/pi/lapem/music/audio.mp3')
                    mixer.music.play()  #Playing Music with Pygame
                    mixer.music.pause() #pausing music file

                    for x in range(3):
                        GPIO.output(LEDPlay, 1)
                        sleep(0.1)
                        GPIO.output(LEDPlay, 0)
                        sleep(0.1)
                else:
                    print "Specif Mode Lan"

                    for x in range(20):
                        GPIO.output(LEDPlay, 1)
                        sleep(0.1)
                        GPIO.output(LEDPlay, 0)
                        sleep(0.1)

                    # subprocess.run (["sudo ifconfig wlan0"])
        else:
	    # print "Nothing"
	    # We Will invert the Play Pause Button,
            # because we have release the button
            oneshot = 0
	    if ToggleButtonPlayPause == 0 :
                CurrentButtonPlayPause = 0
            else:
                CurrentButtonPlayPause = 1

            sleep(0.1)      # wait 0.1 seconds


# this block will run no matter how the try block exits
finally: 
    GPIO.cleanup()  # clean up after yourself

