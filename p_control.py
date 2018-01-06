#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from multiprocessing import Process
import time as t
import math

def main():
  left_motor = ev3.LargeMotor('outC')
  right_motor = ev3.LargeMotor('outB')
  lcd = ev3.Screen()

  ts = ev3.TouchSensor('in2');    assert ts.connected, "Connect a touch sensor to any port" 
  us = ev3.UltrasonicSensor() 

  us.mode='US-DIST-CM'

  units = us.units
  # reports 'cm' even though the sensor measures 'mm'
  separation = 20
  constant = 50
  while not ts.value():    # Stop program by pressing touch sensor button
  
    # US sensor will measure distance to the closest
    # object in front of it.
    distance = us.value()/10  # convert mm to cm
    error = distance - separation      
    
    #Calculate the derivative of the errors

    
    print(str(distance) + " " + units)
    print(str(error) + " " + units)
    lcd.draw.text((10,10), str(distance)+ " " + units)
    lcd.draw.text((10,10), str(error)+ " " + units)

    if distance != separation :  #This is an inconveniently large distance
      output = constant * error + 0 
      if(output > 1000):
        output = 990
      elif (output < -1000):
        output = -990
      else:
        output = constant * error + 0 
        
      left_motor.run_forever(speed_sp=output)
      right_motor.run_forever(speed_sp=output)

if __name__ == '__main__':
    main()
