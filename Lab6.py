import time
import shifter
import random
import RPi.GPIO as GPIO

shift = shifter.Shifter(23,24,25)
x=0

try:
  while 1:
  	val=random.randrange(-1,2,2)
  	x=x+val
  	if x<0 or x>7:
  		shift.shiftByte(-val)
  		shift.shiftByte(-val)
  		x=x-2*val
  	else:
  		shift.shiftByte(val)
  	time.sleep(.05)

except KeyboardInterupt:
  GPIO.cleanup()

finally:
    GPIO.cleanup()
