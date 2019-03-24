import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
 
RELAIS_1_GPIO = 17
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
try:
    while True:
        GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # out
        sleep(1)
        GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
        sleep(1)

except:
    GPIO.output(RELAIS_1_GPIO, GPIO.LOW)