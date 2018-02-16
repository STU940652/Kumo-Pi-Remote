#! /usr/bin/python3

import RPi.GPIO as GPIO
import time

BUTTON_IN = [5, 10, 27, 3]
LED_OUT = [6, 9, 22, 4]

def button_callback(button, e = None):
    time.sleep(0.100)
    button_value = 0
    button_count = 0
    for i in range(len(BUTTON_IN)):
        if not GPIO.input(BUTTON_IN[i]):
            button_value += 2**i
            button_count += 1
    print ("Button", button, button_value, button_count)

    if (button_count):
        for i in range(len(LED_OUT)):
            GPIO.output(LED_OUT[i], not (button_value & 2**i))

# Use BCM pin numbering convention
GPIO.setmode(GPIO.BCM)

# Button 4
# GPIO.setup(BUTTON_IN[3], GPIO.IN) #GPIO 3, Pin 5 #  A physical pull up resistor is fitted on this channel
# GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for g in BUTTON_IN:
    GPIO.setup(g, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(g, GPIO.BOTH, callback=button_callback, bouncetime=100)

for g in LED_OUT:
    GPIO.setup(g, GPIO.OUT)
    GPIO.output(g, 0)

while True:
    time.sleep(0.5)


