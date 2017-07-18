import sys
from time import sleep
import RPi.GPIO as GPIO
import threading


class Stepper:
    """A class representing a stepper motor."""

    # counter for all active instances of this class
    activeMotorCount = 0

    def __init__(self, pins, name, stepdelay, direction, turnLimit):
        self.name = name
        self.stepdelay = stepdelay
        self.direction = direction
        self.isTurning = False
        self.turnCount = 0
        self.turnLimit = turnLimit

        # Save GPIO pin numbers
        self.P1 = pins[0]
        self.P2 = pins[1]
        self.P3 = pins[2]
        self.P4 = pins[3]
        self.pins = pins
        Stepper.activeMotorCount += 1
        print("number of active motors:" + str(Stepper.activeMotorCount))

    def run(self):
        """
        Run the motor for <self.turnCount> steps.

        Turncount is not implemented as a method-parameter so this method
        can more easily be executed in a multithreaded environment
        """
        self.isTurning = True
        while self.isTurning and self.turnCount < self.turnLimit:

            # pin sequence for counter-clockwise rotation.
            if (self.direction == "L"):
                self.turn(self.P4, self.P3, self.P2, self.P1)

            # pin sequence for clockwise rotation.
            elif(self.direction == "R"):
                self.turn(self.P1, self.P2, self.P3, self.P4)

    def stop(self):
        """Stop the motor if it is running."""
        self.isTurning = False

    def turn(self, a, b, c, d):
        """
        Turn on the motor in a half-stepping sequence.

        Note: Full-stepping could be implemented in the future
        """
        # Step1
        GPIO.output(d, True)
        sleep(self.stepdelay)
        GPIO.output(d, False)

        # Step2
        GPIO.output(d, True)
        GPIO.output(c, True)
        sleep(self.stepdelay)
        GPIO.output(d, False)
        GPIO.output(c, False)

        # Step3
        GPIO.output(c, True)
        sleep(self.stepdelay)
        GPIO.output(c, False)

        # Step4
        GPIO.output(b, True)
        GPIO.output(c, True)
        sleep(self.stepdelay)
        GPIO.output(b, False)
        GPIO.output(c, False)

        # Step5
        GPIO.output(b, True)
        sleep(self.stepdelay)
        GPIO.output(b, False)

        # Step6
        GPIO.output(a, True)
        GPIO.output(b, True)
        sleep(self.stepdelay)
        GPIO.output(a, False)
        GPIO.output(b, False)

        # Step7
        GPIO.output(a, True)
        sleep(self.stepdelay)
        GPIO.output(a, False)

        # Step8
        GPIO.output(d, True)
        GPIO.output(a, True)
        sleep(self.stepdelay)
        GPIO.output(d, False)
        GPIO.output(a, False)

        self.turnCount += 1

# This module can be run seperately to demonstrate how to turn the motors.
if __name__ == "__main__":

    # Set pin numbering scheme
    GPIO.setmode(GPIO.BCM)

    # Define GPIO Signals to use
    # Physical Pins used:
    # 7,11,12,13,15,16,18,22
    # GPIO: 4,17,18,27,22,23,24,25
    StepMotorPins1 = [17, 18, 27, 22]
    StepMotorPins2 = [23, 24, 25, 4]

    # Init and start motors
    motor1 = Stepper(StepMotorPins1, "FirstMotor", 0.001, "L", 400)
    motor2 = Stepper(StepMotorPins2, "SecondMotor", 0.001, "L", 400)
    pins = motor1.pins + motor2.pins

    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)

    try:
        motor1Thread = threading.Thread(target=motor1.run)
        motor2Thread = threading.Thread(target=motor2.run)

        motor1Thread.start()
        motor2Thread.start()

        motor1Thread.join()
        motor2Thread.join()

        GPIO.cleanup()
        exit(0)

    except KeyboardInterrupt:

        print "stopped"
        motor1.stop()
        motor2.stop()
        GPIO.cleanup()
        exit(0)
