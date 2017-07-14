from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution = (1280, 720)
camera.start_preview()
sleep(5) 
#TODO : connect LED as a flash and trigger it before taking a picture
camera.capture('/home/pi/Projects/FoodPlate/images/image.jpg')
camera.stop_preview()
