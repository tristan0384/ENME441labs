import time
import shifter

shift = shifter.Shifter(23,24,25)


try:
  while 1:
  	shift.shiftByte()
  	time.sleep(.05)

except:
  GPIO.cleanup()
