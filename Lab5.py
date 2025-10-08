import RPi.GPIO as GPIO
import time
from math import *
GPIO.setmode(GPIO.BCM)
x=1

pins=[]

print(f"Started")

for i in range(2,12):
	GPIO.setup(i,GPIO.OUT,0)
	pins.append(GPIO.PWM(i,500))
	pins[i-2].start(0)

GPIO.setup(26,GPIO.IN,GPIO.PUD_DOWN)

def change(i):
	global x
	x=i
	
GPIO.add_event_detect(
	26,
	GPIO.RISING,
	x=-1,
	1000)
GPIO.add_event_detect(
	26,
	GPIO.RISING,
	x=1,
	1000)

try:
	while(1):
		for i in range(len(pins)):
			#pins[i].ChangeDutyCycle(100)
			pins[i].ChangeDutyCycle((sin(2*pi*.2*time.time()-i*x*pi/11))**2)

except:
	print(f"Ending")
	GPIO.cleanup()













