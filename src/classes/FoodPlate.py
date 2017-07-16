import cv2
import collections
from Camera import Camera
import math
import cmath


class FoodPlate():

    items = collections.deque()

    # Coordinates of the center of the plate
    center = None

    """
    Initializes a Foodplate, calibrates it's center for future calculation
    of FoodPlateItem positions
    """

    def __init__(self):
        #self.camera = Camera()
        self.mostRecentImage = None
        self.items = collections.deque()

        """
        Adds an Item to the FoodPlate
        """

    def addItem(self, item):
        self.items.append(item)

        """
        Removes an Item from the FoodPlate
        """

    def removeItem(self, item):
        self.items.remove(item)

    """
    Turns an Item on the FoodPlate so that it faces a towards a person opening a the fridge.
    """
    def bringItemToFront():
        raise NotImplementedError

    def scanItems():

        mostRecentImage = self.camera.takeImage()
        self.productDetector.detectProducts(mostRecentImage)

    """ 
    Updates the positions of all items after a rotation of <angle> degrees 
    """
    def updateItems(angle):

    	#iterates over all items a
        for item in self.items:
        	#update coordinates on the plate 
            item.coordinates = rotatePoint2D(self.center,item.center,angle)
            #update position measured in DEG
            item.position = item.position+angle;

    """
    Calculates the position of an item in degrees, measured counter clockwise
    """
    def getItemPosition(plateCenter, itemCenter):

        platerCenterPhase = cmath.phase(
            complex(plateCenter.x, plateCenter.y))
        itemCenterPhase = cmath.phase(complex(itemCenter.x, itemCenter.y))

        angle = (plateCenterPhase - itemCenterPhase) * 180 / cmath.pi

        if(angle < 0):
            angle += 360

        return angle

    def rotatePoint2D(centerPoint, point, angle):

        """Rotates a point around another centerPoint. Angle is in degrees. Rotation is counter-clockwise"""
        angle = math.radians(angle)

        # Move to origin
        temp_point = point[0] - centerPoint[0], point[1] - centerPoint[1]

        # Multiply with 2D rotation matrix
        temp_point = (temp_point[0] * math.cos(angle) - temp_point[1] * math.sin(
            angle), temp_point[0] * math.sin(angle) + temp_point[1] * math.cos(angle))

        # move back
        temp_point = temp_point[
            0] + centerPoint[0], temp_point[1] + centerPoint[1]

        return temp_point
