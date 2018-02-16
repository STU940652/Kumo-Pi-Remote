#! /usr/bin/python3

import RPi.GPIO as GPIO
import time
from kumoManager import kumoManager

BUTTON_IN = [5, 10, 27, 3]
LED_OUT = [6, 9, 22, 4]

kumo_sources = {
    1:  14, # Stage 3
    2:  12, # Stage 5
    4:  11, # Stage 7
    8:  13, # Stage 11 (Drum)

    3:   9, # KiPro Out
    6:   4, # FOH Tie18
    12:  8} # DVD GLS SAT

kumo_dest = 4    # Switcher Channel 4

kumo_ip = "10.70.58.25"

kumo_manager = None

def button_callback(button, e = None):
    time.sleep(0.100)
    button_value = 0
    button_count = 0
    for i in range(len(BUTTON_IN)):
        if not GPIO.input(BUTTON_IN[i]):
            button_value += 2**i
            button_count += 1

    if (button_count):
        for i in range(len(LED_OUT)):
            GPIO.output(LED_OUT[i], not (button_value & 2**i))

        if (button_value in kumo_sources):
            print (kumo_sources[button_value])
            if kumo_manager:
                kumo_manager.setChannel(kumo_dest, kumo_sources[button_value])


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
    # This "thread" maintains the link to the Kumo, and gets status updates
    if not kumo_manager:
        time.sleep(10) # Wait 10 seconds and try to re-establish
        kumo_manager = kumoManager(kumo_ip)
    if kumo_manager.online:
        kumo_current_source = kumo_manager.getChannel(kumo_dest)
        for s in kumo_sources:
            if kumo_current_source == kumo_sources[s]:
                for i in range(len(LED_OUT)):
                    GPIO.output(LED_OUT[i], not (s & 2**i))
                break

    else:
        kumo_manager = None
    time.sleep(0.5)


