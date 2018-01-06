#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import time

lcd = ev3.Screen()                   # The EV3 display
rightMotor = ev3.LargeMotor('outB')  # The motor connected to the right wheel
leftMotor = ev3.LargeMotor('outC')   # The motor connected to the left wheel
button = ev3.Button()				 # Any button
camera = ev3.Sensor(address=ev3.INPUT_1)	 # The camera
assert camera.connected, "Error while connecting Pixy camera to port 2"

lcd = ev3.Screen()
ts = ev3.TouchSensor('in2');    assert ts.connected, "Connect a touch sensor to any port" 
us = ev3.UltrasonicSensor() 
us.mode='US-DIST-CM'
units = us.units
# reports 'cm' even though the sensor measures 'mm'

CAMERA_WIDTH_PIXELS = 255
CAMERA_HEIGHT_PIXELS = 255

leftMotor = ev3.LargeMotor('outC')
rightMotor = ev3.LargeMotor('outB')
lcd = ev3.Screen()

ts = ev3.TouchSensor('in2');    assert ts.connected, "Connect a touch sensor to any port" 
us = ev3.UltrasonicSensor() 

us.mode='US-DIST-CM'

units = us.units
# reports 'cm' even though the sensor measures 'mm'

def stop():
    leftMotor.stop()
    rightMotor.stop()
 
 
def maintain_distance():
  separation = 20
  constant = 50
  while not ts.value():    # Stop program by pressing touch sensor button
    # US sensor will measure distance to the closest
    # object in front of it.
    distance = us.value()/10  # convert mm to cm
    error = distance - separation      
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
        
      leftMotor.run_forever(speed_sp=output)
      rightMotor.run_forever(speed_sp=output)
      
    objCount = camera.value(0)	# get the number of objects seen by the camera
    if (objCount > 0):    # if we've seen at least one object
      # get the position and dimensions of the largest object seen
      x = camera.value(1)	# x coordinate of middle of largest object
      y = camera.value(2)	# y coordinate of middle of largest object
      w = camera.value(3)	# width of largest object
      h = camera.value(4)	# height of largest object
        
      print("Found " + str(objCount) + " objects.")
      print("  Largest is at (" + str(x) + "," + str(y) + ")" +
  		    " with width " + str(w) + " pixels" +
    		  " and height " + str(h) + " pixels")
      k = 50
      error1 = CAMERA_WIDTH_PIXELS/2 - w/2
      error2 = CAMERA_WIDTH_PIXELS/2 + w/2
      
      if (x < error1):
            turning_speed = 50 * abs(error1)
            if(abs(error1)*k > 1000):
              turning_speed = 990
            leftMotor.run_forever(speed_sp = turning_speed)
            rightMotor.run_forever(speed_sp = 0)
            
      elif (x > error2):
            turning_speed = 50 * abs(error2)
            if(abs(error2)*k > 1000):
              turning_speed = 990
            leftMotor.run_forever(speed_sp = 0)
            rightMotor.run_forever(speed_sp = turning_speed )
      
            
      else:
            leftMotor.run_forever(speed_sp = output)
            rightMotor.run_forever(speed_sp = output)
    else:
      leftMotor.run_forever(speed_sp=output)
      rightMotor.run_forever(speed_sp =output)


def setCameraMode(sigNum):
	camera.mode = 'SIG'+str(sigNum)   

          
def main():
  setCameraMode(5)
  while (not button.any()):
    maintain_distance()
    # Add a delay to reduce frequency of printing info to screen
    time.sleep(2)
   
if __name__ == '__main__':
  main()
    
      
