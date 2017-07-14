import sys
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

time = 0.001
directionMotor1 = 0
directionMotor2 = 0


if len(sys.argv)>1:
    directionMotor1 = sys.argv[1]
    directionMotor2 = sys.argv[2]
else:
    print ("param direction missing")

# Define GPIO Signals to use
# Physical Pins used:
# 7,11,12,13,15,16,18,22
# GPIO: 4,17,18,27,22,23,24,25
StepMotorPins1 = [17,18,27,22]
StepMotorPins2 = [23,24,25,4]

# Set all pins as output
for pin in StepMotorPins1:
    print ("Setup pin %s of motor 1" %(pin))
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, False)

for pin in StepMotorPins2:
    print ("Setup pin %s of motor2" %(pin))
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,False)

if directionMotor1 == "R":
    A = StepMotorPins1[3]
    B = StepMotorPins1[2]
    C = StepMotorPins1[1]
    D = StepMotorPins1[0]

elif directionMotor1 == "L":
    A = StepMotorPins1[0]
    B = StepMotorPins1[1]
    C = StepMotorPins1[2]
    D = StepMotorPins1[3]

if directionMotor2 == "R":
    E = StepMotorPins2[3]
    F = StepMotorPins2[2]
    G = StepMotorPins2[1]
    H = StepMotorPins2[0]


elif directionMotor2 == "L":
    E = StepMotorPins2[0]
    F = StepMotorPins2[1]
    G = StepMotorPins2[2]
    H = StepMotorPins2[3]

#Motor1
def StepMotor1():
    #Step1
    GPIO.output(D, True)
    sleep (time)
    GPIO.output(D, False)

    #Step2
    GPIO.output(D, True)
    GPIO.output(C, True)
    sleep (time)
    GPIO.output(D, False)
    GPIO.output(C, False)
    
    #Step3
    GPIO.output(C, True)
    sleep (time)
    GPIO.output(C, False)
    
    #Step4
    GPIO.output(B, True)
    GPIO.output(C, True)
    sleep (time)
    GPIO.output(B, False)
    GPIO.output(C, False)
        
    #Step5
    GPIO.output(B, True)
    sleep (time)
    GPIO.output(B, False)
    
    #Step6
    GPIO.output(A, True)
    GPIO.output(B, True)
    sleep (time)
    GPIO.output(A, False)
    GPIO.output(B, False)
    
    #Step7
    GPIO.output(A, True)
    sleep (time)
    GPIO.output(A, False)
    
    #Step8
    GPIO.output(D, True)
    GPIO.output(A, True)
    sleep (time)
    GPIO.output(D, False)
    GPIO.output(A, False)

#Motor2
def StepMotor2():
    
    #Step1
    GPIO.output(H, True)
    sleep (time)
    GPIO.output(H, False)

    #Step2
    GPIO.output(H, True)
    GPIO.output(G, True)
    sleep (time)
    GPIO.output(H, False)
    GPIO.output(G, False)
   
    #Step3
    GPIO.output(G, True)
    sleep (time)
    GPIO.output(G, False)

    #Step4
    GPIO.output(F, True)
    GPIO.output(G, True)
    sleep (time)
    GPIO.output(F, False)
    GPIO.output(G, False)

    #Step5
    GPIO.output(F, True)
    sleep (time)
    GPIO.output(F, False)
    
    #Step6
    GPIO.output(E, True)
    GPIO.output(F, True)
    sleep (time)
    GPIO.output(E, False)
    GPIO.output(F, False)

    #Step7
    GPIO.output(E, True)
    sleep (time)
    GPIO.output(E, False)

    #Step8
    GPIO.output(H, True)
    GPIO.output(E, True)
    sleep (time)
    GPIO.output(H, False)
    GPIO.output(E, False)

for i in range (2056):
    try:
        StepMotor1();
        StepMotor2();
        print (i)
    except KeyboardInterrupt:
        print ("stopped")
        GPIO.cleanup()
        exit(0);


GPIO.cleanup()
