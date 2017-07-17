from picamera import PiCamera
import io
import np
from time import sleep
import picamera.array
import cv2

class Camera():

    def __init__(self, resolution=(1920, 1088)):
    	self.resolution = resolution
       
    
    def takeImage(self,path):
    	with picamera.PiCamera() as camera:
			camera.resolution = (1920, 1080)
			camera.start_preview()
			sleep(1)
			camera.capture(path)
			camera.stop_preview()

