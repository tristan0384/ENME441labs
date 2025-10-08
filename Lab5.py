import RPi.GPIO as GPIO
import time
from math import *
GPIO.setmode(GPIO.BCM)
pins=[]

print(f"Started")

for i in range(2,12):
	GPIO.setup(i,GPIO.OUT,initial=0)
	pins.append(GPIO.PWM(i,500))
	pins[i-2].start(0)

try:
	while(1):
		for i in range(len(pins)):
			#pins[i].ChangeDutyCycle(100)
			pins[i].ChangeDutyCycle((sin(2*pi*.2*time.time()-i*pi/11))**2)

except:
	print(f"Ending")
	GPIO.cleanup()







