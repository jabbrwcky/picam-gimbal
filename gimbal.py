#!/usr/bin/env python

from time import sleep


import RPIO
import readchar

print(RPIO.RPI_REVISION)

MOTOR_X = [ 4, 17, 27, 22 ]
MOTOR_Y = [ 14, 15, 18, 23 ]

X=1
Y=0
UP=1
DOWN=0
LEFT=1
RIGHT=0

STEPS = [
    [0,0,0,1],
    [0,0,1,1],
    [0,0,1,0],
    [0,1,1,0],
    [0,1,0,0],
    [1,1,0,0],
    [1,0,0,0],
    [1,0,0,1]
]

step_idx=[0,0]

# Mapping of endstops
# [X_min, X_max, Y_min, Y_max]
ENDSTOPS = [ 7, 8, 9, 10 ]
endstop = [ 0, 0, 0, 0 ] 

def endstop_hit(gpio_id, value):
    idx = ENDSTOPS.index(gpio_id)
    endstop[idx] = value
    print("Endstop hit %d: %d :: %s" % (gpio_id, value, endstop))

def step(axis, direction):
    if axis:
        for idx in range(0,len(MOTOR_X)):
            RPIO.output(MOTOR_X[idx], STEPS[step_idx[axis]][idx])
    else:
        for idx in range(0,len(MOTOR_Y)):
            RPIO.output(MOTOR_Y[idx], STEPS[step_idx[axis]][idx])

    if direction:
        step_idx[axis] = (step_idx[axis] + 1) % len(STEPS)
    
    else: 
        step_idx[axis] = (step_idx[axis] - 1) % len(STEPS)

    sleep(0.001)

try:
    for gpio in MOTOR_X + MOTOR_Y:
        RPIO.setup(gpio, RPIO.OUT, initial=RPIO.LOW)

    for gpio in ENDSTOPS:
        RPIO.setup(gpio, RPIO.IN, pull_up_down=RPIO.PUD_DOWN)
        RPIO.add_interrupt_callback(gpio, endstop_hit, pull_up_down=RPIO.PUD_DOWN, debounce_timeout_ms=10, threaded_callback=True)

    RPIO.wait_for_interrupts(threaded=True)

    while(True):
        k = readchar.readkey()
        if k == '\x03':
            break
        elif k == readchar.key.UP:
            for i in range(0,8*100):
                step(Y,UP)
        elif k == readchar.key.DOWN:
            for i in range(0,8*100):
                step(Y,DOWN)
        elif k == readchar.key.LEFT:
            for i in range(0,8*100):
                step(X,LEFT)
        elif k == readchar.key.RIGHT:
            for i in range(0,8*100):
                step(X,RIGHT)
#        else:
#            for p in MOTOR_X+MOTOR_Y:
#                RPIO.output(p, RPIO.LOW)


except KeyboardInterrupt:
    # Exit on Ctrl-C
    pass
      	
finally:
    RPIO.cleanup()
