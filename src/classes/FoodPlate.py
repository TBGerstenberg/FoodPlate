import cv2
import collections
from Camera import Camera


class FoodPlate():
    
    items = collections.deque()

	"""Initializes a Foodplate, calibrates it's center for future calculation of FoodPlateItem positions"""
	def __init__(self):
		self.camera = Camera()
		self.mostRecentImage = None
		self.productDetector = productDetector

	""" 
	Adds an Item to the FoodPlate
	"""
	def addItem(item):
		items.append(item)

	"""
	Removes an Item from the FoodPlate
	"""
    
	def removeItem(item):
        index = items.index(item)
		items.remove(index)

    def sortItems():
        

	"""
	Turns an Item on the FoodPlate so that it faces a towards a person opening a the fridge. 
	"""
	def bringItemToFront():
		raise NotImplementedError;


	def scanItems():

		mostRecentImage = self.camera.takeImage()
		self.productDetector.detectProducts(mostRecentImage)


	def calibratePlateCenter(self):
		#Shoot an image
		self.mostRecentImage = self.camera.takeImage()


