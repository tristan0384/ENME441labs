import RPi.GPIO as GPIO
import time


class Shifter:
  def __init__(self, serialPin, latchPin, clockPin):
    self.serialPin=serialPin
    self.clockPin=clockPin
    self.latchPin=latchPin
    self.pattern=0b10000000

    GPIO.setmode(GPIO.BCM)


    GPIO.setup(self.serialPin, GPIO.OUT)
    GPIO.setup(self.latchPin, GPIO.OUT, initial=0)  # start latch & clock low
    GPIO.setup(self.clockPin, GPIO.OUT, initial=0)  



  def shiftByte(self,shift):
    if shift == 1:
      self.pattern >>= 1
    elif shift == -1:
      self.pattern <<= 1
    else:
      return
    self._ping()




  def _ping(self):
    for i in range(8):
      GPIO.output(self.serialPin, self.pattern & (1<<i))
      GPIO.output(self.clockPin,1)       # ping the clock pin to shift register data
      time.sleep(0)
      GPIO.output(self.clockPin,0)

    GPIO.output(self.latchPin, 1)        # ping the latch pin to send register to output
    time.sleep(0)
    GPIO.output(self.latchPin, 0)

