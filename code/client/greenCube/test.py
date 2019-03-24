#! /usr/bin/env python
import RPi.GPIO as GPIO
import sys
import time


def zap():
    GPIO.output(laser, GPIO.HIGH)
    print("Laser on")

def zip():
    GPIO.output(laser, GPIO.LOW)
    print("Laser off")

# Set leds GPIO
ir = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(ir, GPIO.IN)

go = 1
i = 1
while(go==1):

    if (GPIO.input(ir) == 0):
        print(i)
        i+=1

print("Damn!")
