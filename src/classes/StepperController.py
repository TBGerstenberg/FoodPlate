import RPi.GPIO as GPIO
import threading
import atexit

from Stepper import Stepper
"""
	StepperController for the FoodPlate that controls two 5V Steppers
"""


class StepperController():
    def __init__(self):
        # Set pin numbering scheme
        GPIO.setmode(GPIO.BCM)
        # Define GPIO Signals to use
        # Physical Pins used:
        # 7,11,12,13,15,16,18,22
        # GPIO: 4,17,18,27,22,23,24,25
        StepMotorPins1 = [17, 18, 27, 22]
        StepMotorPins2 = [23, 24, 25, 4]
        self.stepper1 = Stepper(StepMotorPins1, "FirstMotor", 0.001, "L", 3200)
        self.stepper2 = Stepper(StepMotorPins2, "SecondMotor", 0.001, "L",
                                3200)
        pins = self.stepper1.pins + self.stepper2.pins
        atexit.register(self.cleanup)

        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

    def turn(self, angle, direction):

        turnLimit = self.angleToSteps(angle)
        self.stepper1.turnLimit = turnLimit
        self.stepper1.direction = direction

        self.stepper2.direction = direction
        self.stepper2.turnLimit = turnLimit

        motor1Thread = threading.Thread(target=self.stepper1.run)
        motor2Thread = threading.Thread(target=self.stepper2.run)

        motor1Thread.start()
        motor2Thread.start()

        motor1Thread.join()
        motor2Thread.join()

    """ Converts a given angle in euler-angles to a number of steps the two 
	motors need to turn the FoodPlate for that given angle"""

    def angleToSteps(self, angle):
        return 8.333333 * angle

    def cleanup(self):
        print ("Motors stopped and pins freed up")
        self.stepper1.stop()
        self.stepper2.stop()
        GPIO.cleanup()
        exit(0)
