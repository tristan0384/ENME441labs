import Bug
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  

bug=Bug.Bug()
x2old=GPIO.input(20)


try:
	while(1):
		x1=GPIO.input(16)
		x2=GPIO.input(20)
		x3=GPIO.input(21)

		if x1:
			bug.start()
		else:
			bug.stop()

		if not x2==x2old:
			bug.wrap()

		if x3:
			bug.speed(True)
		else:
			bug.speed(False)
			
		x2old=x2







except KeyboardInterrupt:
  GPIO.cleanup()

finally:
    GPIO.cleanup()
