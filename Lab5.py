import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
start=time.time()
pins=[]

for i in range(2,11):
	pins.append(obj=GPIO.PWM(i,500))
	#GPIO.setup(i,GPIO.OUT,initial=0)

while(1):
	for i in range(10):
		pins(i).ChangeDutyCycle((sin(2*pi*.2*time.time()-i*pi/11))^2)
