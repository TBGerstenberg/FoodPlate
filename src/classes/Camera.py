from picamera import PiCamera
from time import sleep
import picamera.array

class Camera():

    """
    Simple wrapper for respberry pi camera functionality with using picam.
    """
    def capture_image(self,path):
    	"""Capture an image and write it to <path>."""
    	with picamera.PiCamera() as camera:
            camera.resolution = (1920, 1380)
            camera.rotation = 180
            camera.start_preview()
            print("sleeping for 5 seconds to let camera calibrate focus and lighting")
            for i in xrange(5,-1,-1):
                sleep(1)
                print i
            camera.capture(path)
            camera.stop_preview()

