#!/usr/bin/env python3
'''COM2009-3009 EV3DEV TEST PROGRAM'''

# Connect left motor to Output C and right motor to Output B
# Connect an ultrasonic sensor to Input 3

import os
import sys
import time
import ev3dev.ev3 as ev3
import math

# state constants
ON = True
OFF = False


def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)


def reset_console():
    '''Resets the console to the default state'''
    print('\x1Bc', end='')


def set_cursor(state):
    '''Turn the cursor on or off'''
    if state:
        print('\x1B[?25h', end='')
    else:
        print('\x1B[?25l', end='')


def set_font(name):
    '''Sets the console font

    A full list of fonts can be found with `ls /usr/share/consolefonts`
    '''
    os.system('setfont ' + name)


def main():
    '''The main function of our program'''

    # set the console just how we want it
    reset_console()
    set_cursor(OFF)
    set_font('Lat15-Terminus24x12')

    # display something on the screen of the device
    print('Hello World!')

    # print something to the output panel in VS Code
    debug_print('Hello VS Code!')

    # announce program start
   # ev3.Sound.speak('Test program starting!').wait()

    # set the motor variables
    mb = ev3.LargeMotor('outB')
    mc = ev3.LargeMotor('outC')
    sp = -25
    diff = -25

    # set the ultrasonic sensor variable
    us3 = ev3.UltrasonicSensor('in3')

    #Code for Q2, take sample of distance every 10 msec and work out mean,min,max,standard deviation  
    for i in range (0, 10):
        #Time loop begins
        ds = []
        total = 0
        #Take 1000 samples 
        for j in range (0,1000):
            starttime = time.time()
            dis = us3.value()
            ds.append(dis)
            total+=dis
            if j < 0:
                time.sleep(.01 - (time.time()-starttime))
        #work out min, max, mean, and standard deviation
        dsmin = min(ds)
        dsmax = max(ds)
        dsmean =total/1000
        dsVar = 0
        for val in ds:
            dsVar += pow(abs(val-dsmean),2)
        dsStdDev= math.sqrt(dsVar/1000)
        #print min, max, mean, and standard deviation
        debug_print('min ',i, " = ", dsmin)
        debug_print('max ', i, " = ",dsmax)
        debug_print('mean ',i, " = ",dsmean)
        debug_print('standard deviation ', i, ' = ', dsStdDev)
        #work out how long the function took and calcualte how much delat is needed for 10ms loop.
        
    
    # program loop
    # for x in range (1, 5):
        
    #     # fetch the distance
    #     ds = us3.value()
            
    #     # display the distance on the screen of the device
    #     print('Distance =',ds)

    #     # print the distance to the output panel in VS Code
    #     debug_print('Distance =',ds)
        
    #     # announce the distance
         #   ev3.Sound.speak(ds)

    #     # move
    #     mb.run_direct(duty_cycle_sp=sp-diff)
    #     mc.run_direct(duty_cycle_sp=sp+diff)
    #     time.sleep(1)

    #     # stop
    #     mb.run_direct(duty_cycle_sp=0)
    #     mc.run_direct(duty_cycle_sp=0)
        
    #     # reverse direction
    #     sp = -sp
    #     diff = -diff
    
    # # announce program end
    # ev3.Sound.speak('Test program ending').wait()

if __name__ == '__main__':
    main()
