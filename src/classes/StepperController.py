import sys
import signal
from time import sleep
import RPi.GPIO as GPIO
import threading
import stepper.py
import atexit


class StepperContoller:

	self.stepper1
	self.stepper2

	def __init__(self):

		# Set pin numbering scheme
	    GPIO.setmode(GPIO.BCM)

	    # Define GPIO Signals to use
	    # Physical Pins used:
	    # 7,11,12,13,15,16,18,22
	    # GPIO: 4,17,18,27,22,23,24,25
	    StepMotorPins1 = [17, 18, 27, 22]
	    StepMotorPins2 = [23, 24, 25, 4]

		stepper1 = Stepper(StepMotorPins1, "FirstMotor", 0.001, "L", 400)
		stepper2 = Stepper(StepMotorPins2, "SecondMotor", 0.001, "L", 400)
		pins = motor1.pins + motor2.pins

		for pin in pins:
    		GPIO.setup(pin, GPIO.OUT)
        	GPIO.output(pin, False)

        atexit.register(self.cleanup)

    def turn(angle):
    	motor1Thread = threading.Thread(target=motor1.run)
	 	motor2Thread = threading.Thread(target=motor2.run)

	 	motor1Thread.start()
	 	motor2Thread.start()

	 	motor1Thread.join()
	 	motor2Thread.join()

	 def cleanup:
	 	print "Motors stopped and pins freed up"
	 	motor1.stop()
	 	motor2.stop()
	 	GPIO.cleanup()
        exit(0)
