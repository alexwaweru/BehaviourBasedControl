#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from multiprocessing import Process
import time as t
import math
from functools import reduce

def main():
  left_motor = ev3.LargeMotor('outC')
  right_motor = ev3.LargeMotor('outB')
  lcd = ev3.Screen()

  ts = ev3.TouchSensor('in2');    assert ts.connected, "Connect a touch sensor to any port" 
  us = ev3.UltrasonicSensor() 

  us.mode='US-DIST-CM'

  units = us.units
  # reports 'cm' even though the sensor measures 'mm'
  
  errors = []
  errors.append(0)
  while not ts.value():    # Stop program by pressing touch sensor button
    # US sensor will measure distance to the closest
    # object in front of it.
    separation = 20
    distance = us.value()/10  # convert mm to cm
    error = distance - separation 
    err = errors.pop()
    de = error - err
    errors.append(err)
    errors.append(error)

    #Calculate the integral of error(sum of errors)
    sum_of_errors = reduce(lambda x, y: x+y, errors)
    
    print(str(distance) + " " + units)
    print(str(error) + " " + units)
    lcd.draw.text((10,10), str(distance)+ " " + units)
    lcd.draw.text((10,10), str(error)+ " " + units)

    if distance != separation:  #This is an inconveniently large distance
      output = (50 * (error)) + (de) + (sum_of_errors) + 0
      if(output > 1000):
        output = 990
      elif (output < -1000):
        output = -990
        
      left_motor.run_forever(speed_sp=output)
      right_motor.run_forever(speed_sp=output)

if __name__ == '__main__':
    main()

