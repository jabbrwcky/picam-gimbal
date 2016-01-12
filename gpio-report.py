#!/usr/bin/env python

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

for pin in range(1,27):
    print("%d: %s" % (pin, GPIO.gpio_function(pin)))

# try:
	
# finally:
# GPIO.cleanup()
