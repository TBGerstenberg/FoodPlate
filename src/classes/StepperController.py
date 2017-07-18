import RPi.GPIO as GPIO
import threading
from Stepper import Stepper


class StepperController():
    """
    StepperController for the FoodPlate that controls two 5V Steppers.
    """

    def __init__(self):
        """
        Initialize a steppercontroller with two motors.

        Note: This uses the BCM numbering scheme to assign pin numers on
        a 26-Pin GPIO Header.
        """

        # Set pin numbering scheme
        GPIO.setmode(GPIO.BCM)
        # Define GPIO Signals to use
        # Physical Pins used:
        # 7,11,12,13,15,16,18,22
        # GPIO: 4,17,18,27,22,23,24,25
        first_motor_pins = [17, 18, 27, 22]
        second_motor_pins = [23, 24, 25, 4]
        self.stepper1 = Stepper(first_motor_pins, "FirstMotor", 0.001, "L",
                                3200)
        self.stepper2 = Stepper(second_motor_pins, "SecondMotor", 0.001, "L",
                                3200)

    def turn(self, angle, direction):
        """Turn all motors controlled by this instance for <angle> degrees."""
        print("Rotating for " + str(angle) + " degrees. \n")

        pins = self.stepper1.pins + self.stepper2.pins

        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

        turn_limit = self.angle_to_steps(angle)
        self.stepper1.turnLimit = turn_limit
        self.stepper1.direction = direction

        self.stepper2.direction = direction
        self.stepper2.turnLimit = turn_limit

        first_motor_thread = threading.Thread(target=self.stepper1.run)
        second_motor_thread = threading.Thread(target=self.stepper2.run)

        first_motor_thread.start()
        second_motor_thread.start()

        first_motor_thread.join()
        second_motor_thread.join()

        print("Motors stopped and pins freed up")
        self.stepper1.stop()
        self.stepper2.stop()

        GPIO.cleanup()

    def angle_to_steps(self, angle):
        """Convert a given angle in euler-angles to a number of steps.

        These steps have been calculated for a plate with diameter of 38.5cm
        the two
        motors need to turn the FoodPlate for that given angle
        """
        return 8.333333 * angle
