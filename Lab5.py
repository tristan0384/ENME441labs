import RPi.GPIO as GPIO
import time
import math
from math import *
GPIO.setmode(GPIO.BCM)
pins=[]

print(f"Started")

for i in range(2,11):
	GPIO.setup(i,GPIO.OUT,initial=0)
	pins.append(GPIO.PWM(i,500))
	

try:
	while(1):
		for i in range(10):
			pins[i].ChangeDutyCycle((sin(2*pi*.2*time.time()-i*pi/11))^2)

except KeyboardInterrupt:
	print(f"Ending")
	GPIO.cleanup()
