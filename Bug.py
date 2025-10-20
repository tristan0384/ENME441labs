import time
import random
import shifter
import RPi.GPIO as GPIO

class Bug:
	def __init__(self,timestep=.1,x=3,isWrapOn=False):
		self.timestep=timestep
		self.first=timestep
		self.x=x
		self.isWrapOn=isWrapOn

	__shifter=shifter.Shifter(23,24,25)

	def wrap(self):
		if self.isWrapOn==False:
			self.isWrapOn=True
		else:
			self.isWrapOn=False


	def speed(self, on):
		if on==True:
			self.timestep=self.first/3
		else:
			self.timestep=self.first




	def start(self):
		val=random.randrange(-1,2,2)
		if self.isWrapOn==False:
		  	self.x=self.x+val
		  	if self.x<0 or self.x>7:
		  		__shifter.shiftByte(-val)
		  		self.x=self.x-(2*val)
		  	else:
		  		__shifter.shiftByte(val)
		  	time.sleep(self.timestep)
		else:
		  	self.x=self.x+val
		  	if self.x<0 or self.x>7:
		  		for i in range(7):
		  			__shifter.shiftByte(-val)
		  		self.x=self.x-(8*val)
		  	else:
		  		__shifter.shiftByte(val)
		  	time.sleep(self.timestep)


	def stop(self):
		pattern=0b00000000
		for i in range(8):
	      GPIO.output(23, pattern & (1<<i))
	      GPIO.output(25,1)       # ping the clock pin to shift register data
	      time.sleep(0)
	      GPIO.output(25,0)
	    GPIO.output(24, 1)        # ping the latch pin to send register to output
	    time.sleep(0)
	    GPIO.output(24, 0)



