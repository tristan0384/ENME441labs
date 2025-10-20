import time
import shifter
import RPi.GPIO as GPIO

shift = shifter.Shifter(23,24,25)


try:
  while 1:
  	shift.shiftByte()
  	time.sleep(.05)

except KeyboardInterupt:
  GPIO.cleanup()

finally:
    GPIO.cleanup()
