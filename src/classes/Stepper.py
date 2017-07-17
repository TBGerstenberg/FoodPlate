import sys
import signal
from time import sleep
import RPi.GPIO as GPIO
import threading
import logging


class Stepper:

    'A class representing a stepper motor'
    activeMotorCount = 0

    def __init__(self, pins, name, stepdelay, direction, turnLimit):
        self.name = name
        self.stepdelay = stepdelay
        self.direction = direction
        self.isTurning = False
        self.turnCount = 0
        self.turnLimit = turnLimit
        self.P1 = pins[0]
        self.P2 = pins[1]
        self.P3 = pins[2]
        self.P4 = pins[3]
        self.pins = pins
        Stepper.activeMotorCount += 1
        print("number of active motors:" + str(Stepper.activeMotorCount))

    def run(self):
        self.isTurning = True
        while self.isTurning and self.turnCount < self.turnLimit:

            if (self.direction == "L"):
                self.turn(self.P4, self.P3, self.P2, self.P1)

            elif(self.direction == "R"):
                self.turn(self.P1, self.P2, self.P3, self.P4)


        #print(self.name + "at step :  " + str(self.turnCount))

    def stop(self):
        self.isTurning = False

    def turn(self, A, B, C, D):

        # Step1
        GPIO.output(D, True)
        sleep(self.stepdelay)
        GPIO.output(D, False)

        # Step2
        GPIO.output(D, True)
        GPIO.output(C, True)
        sleep(self.stepdelay)
        GPIO.output(D, False)
        GPIO.output(C, False)

        # Step3
        GPIO.output(C, True)
        sleep(self.stepdelay)
        GPIO.output(C, False)

        # Step4
        GPIO.output(B, True)
        GPIO.output(C, True)
        sleep(self.stepdelay)
        GPIO.output(B, False)
        GPIO.output(C, False)

        # Step5
        GPIO.output(B, True)
        sleep(self.stepdelay)
        GPIO.output(B, False)

        # Step6
        GPIO.output(A, True)
        GPIO.output(B, True)
        sleep(self.stepdelay)
        GPIO.output(A, False)
        GPIO.output(B, False)

        # Step7
        GPIO.output(A, True)
        sleep(self.stepdelay)
        GPIO.output(A, False)

        # Step8
        GPIO.output(D, True)
        GPIO.output(A, True)
        sleep(self.stepdelay)
        GPIO.output(D, False)
        GPIO.output(A, False)

        self.turnCount += 1


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
