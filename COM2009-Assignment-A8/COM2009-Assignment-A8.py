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

def measure_distance(us3):
 #Code for Q2, take sample of distance every 10 msec and work out mean,min,max,standard deviation  
    #Time loop begins
    total = 0
    #Take 1000 samples 
    for j in range (0,10):
        starttime = time.time()
        dis = us3.value()
        total+=dis
        if j < 0:
            time.sleep(0.001 - (time.time()-starttime))
    #work out min, max, mean, and standard deviation
    dsmean =total/10
    #work out how long the function took and calcualte how much delat is needed for 10ms loop.
    return dsmean

    

def main():
    '''The main function of our program'''
    # set the console just how we want it
    reset_console()
    set_cursor(OFF)
    set_font('Lat15-Terminus24x12')

    # display something on the screen of the device
    print('Begin the maze!')

    # print something to the output panel in VS Code
    debug_print('Begin the maze!')

    # set the motor variables
    mb = ev3.LargeMotor('outB')
    mc = ev3.LargeMotor('outC')
    # set the ultrasonic sensor variable
    us3 = ev3.UltrasonicSensor('in3')
    us2 = ev3.UltrasonicSensor('in2')
    
    
    #Set values
    Kp = 3 * 100
    Ki = 9.6* 100
    Kd = 0.234375 * 100
    integral = 0
    lastError = 0
    lastGoal = 0
    derivative = 0
    dT= 0.2
    sp = 50
    while True:
        starttime = time.time()
        #pid controller 
        rightDis = measure_distance(us2)
        leftDis = measure_distance(us3)
        goal = (leftDis + rightDis) / 2
       
        if goal != lastGoal:   
            integral = 0
            derivative = 0  
        
        #take 100 samples over 1 second
        dis = leftDis
        error = dis - goal
        #set integral to 0 when error changes sign
        if (math.copysign(1, lastError) != math.copysign(1, error)):
            integral = 0
        integral = ((2*integral)/3) + error
        derivative = error - lastError
        move = (Kp * error) + (Ki * integral * dT) + (Kd * derivative/dT)
        move = move  / 100
        if move > 25:
            move = 25
        if move < -25:
            move = -25
        if dis == goal:
            mb.run_direct(duty_cycle_sp=0)
            mc.run_direct(duty_cycle_sp=0)
        else: 
            mb.run_direct(duty_cycle_sp= sp+move)
            mc.run_direct(duty_cycle_sp= sp-move)
        lastError = error
        lastGoal = goal
        debug_print("left: " , leftDis, " right: ", rightDis, " goal", goal, " dis", dis)
        time.sleep(dT - (time.time() - starttime))
          


if __name__ == '__main__':
    main()
