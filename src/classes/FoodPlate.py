import cv2
from classes.Node import UnorderedList
from Camera import Camera
import math
import cmath
from classes.ProductDetector import ProductDetector
from classes.FoodPlateItem import FoodPlateItem
from classes.StepperController import StepperController
from time import sleep
from math import atan2, degrees, pi

class FoodPlate():

    def __init__(self):
        """
        Initialize a Foodplate, calibrates it's center for future calculation
        of FoodPlateItem positions.
        """
        self.camera = Camera()
        self.mostRecentImage = None
        self.items = UnorderedList()
        self.productDetector = ProductDetector()
        self.plateCenter = self.productDetector.imageCenter
        self.stepperController = StepperController()
        #self.getAngle()

    def getItem(self, item):
        self.items.getItem(item)

    def addItem(self, item):
        """Add an Item to the FoodPlate."""
        self.items.addItem(item)

    def removeItem(self, item):
        """Remove an Item from the FoodPlate."""
        self.remove(item)

    def size(self):
        """Get the number of items currently stored on the FoodPlate."""
        self.items.size()

    def setFoodPlateItems(self):
        """Mock-Method: Create a set of FoodPlateItems and assigns them to the items found on the plate."""
        itemNames = []

        foodPlateItem1 = FoodPlateItem(
            "2012-07-18T12:00:00Z", 1342605600, "Marmelade", 0, ())
        #foodPlateItem2 = FoodPlateItem(
        #    "2009-05-21T12:00:00Z", 1242900000, "Erbsen", 0, ())
        #foodPlateItem3 = FoodPlateItem(
        #    "2008-02-21T12:00:00Z", 1203591600, "Champignon", 0, ())


        # foodPlateItem4 = FoodPlateItem(
        #      "2007-01-25T12:00:00Z", 1169722800, "Thunfisch", 0, ())
        # foodPlateItem5 = FoodPlateItem(
        #     "2013-04-13T12:00:00Z", 1365847200, "GoetterSpeise", 0, ())
        # foodPlateItem6 = FoodPlateItem(
        #    "2011-03-10T12:00:00Z", 1299754800,"Honig", 0, ())
        # foodPlateItem7 = FoodPlateItem(
        #     "2011-02-13T12:00:00Z", 1297594800, "Batterie", 0, ())

        for item, value in self.productDetector.foundItems.items():
            foodPlateItem = eval("foodPlateItem" + str(item))
            foodPlateItem.setCenter(value)
            angle = self.getAngle(
                self.plateCenter, foodPlateItem.center)

            print ("Angle of:" + foodPlateItem.name + "is" + str(angle))
            foodPlateItem.setPositionAngle(angle)
            itemNames.append(foodPlateItem.name)

        self.productDetector.drawNames(itemNames)
        self.addItem(foodPlateItem1)
        #self.addItem(foodPlateItem2)
        #self.addItem(foodPlateItem3)
        #self.addItem(foodPlateItem4)
        #self.addItem(foodPlateItem5)
        #self.addItem(foodPlateItem6)

        # print(self.items.size())
        # print(self.items.getItem(2).__dict__)

    def bringItemToFront(self):
        """
        Turn an Item on the FoodPlate so that it faces a towards a person
        opening a the fridge.
        """

        # detect all items on the plate
        self.scanItems()

        # find the one that expires first
        itemWithEarliestExpiry = self.findNextSpoilingItem()

        print("Item with min expiry date :" + itemWithEarliestExpiry.name)

        # calculate where the item is positioned on the plate
        angle = itemWithEarliestExpiry.positionAngle

        # 0 degrees is defined at the backside of the plate
        # we want the item to be place at the front of the plate
        # angle += 180
        turnAngle = 0
        turnDirection = None

        if angle >= 0 and angle <= 180:
            turnAngle = 180 - angle
            turnDirection = "R"          

        elif angle < 0 and angle > -180:
            turnAngle = 180 - math.fabs(angle)
            turnDirection = "L"


        # if angle > 0 and angle < 90:
        #     turnAngle = 90 + angle
        #     turnDirection = "L"

        # elif angle > 90 and angle < 180:
        #     turnAngle = angle + 90
        #     turnDirection = "R"

        # elif angle > -180 and angle < -90:
        #     turnAngle = math.fabs(angle) - 90
        #     turnDirection = "L"

        # elif angle > -90 and angle >= 0:
        #     turnAngle = 90 - math.fabs(angle)
        #     turnDirection = "L"

        print(itemWithEarliestExpiry.name + "should turn for " + str(turnAngle) + "Degrees")
        self.rotate(turnAngle,turnDirection)

        # turn the motors to position item on the front of the plate
        #if angle < 0:
        #    angle = math.fabs(angle)
        #    self.rotate(angle, "R")
        #else:
        #    self.rotate(angle, "L")

        print("Angle between plate center and" + itemWithEarliestExpiry.name +  " is: " + str(angle))

        # print("FoodPlate sleeping")
        # sleep(60)
        # print ("FoodPlate woke up")
        # self.scanItems()

        print("Scan beendet")

    def scanItems(self):
        """Take an image and searches for products on the plate."""

        # take image of the plate
        mostRecentImage = self.camera.takeImage(
            '/home/pi/Projects/FoodPlate/images/raw_input/input.jpg')

        # detect items on the plate
        self.productDetector.detectProducts(mostRecentImage)

        # Fill item list
        self.setFoodPlateItems()

    def updateItems(self, angle):
        """Update the positions of all items after a rotation of <angle> degrees."""

        # iterate over all items that are saved
        for item in self.items:

                # update item coordinate after a rotation of <angle> degrees
            item.coordinates = self.rotatePoint2D(self.center, item.center, angle)

            # update position measured in DEG
            item.position = item.position + angle


    # def getItemPosition(self, plateCenter, itemCenter):
    #     """Calculates the position of an item in degrees, measured counter clockwise."""

    #     plateCenterPhase = cmath.phase(
    #         complex(plateCenter[0], plateCenter[1]))
    #     itemCenterPhase = cmath.phase(complex(itemCenter[0], itemCenter[1]))

    #     angle = (plateCenterPhase - itemCenterPhase) * 180 / cmath.pi

    #     return angle

    def rotatePoint2D(self, centerPoint, point, angle):
        """Rotates a point around a given center in 2D space"""

        #Rotates a point around another centerPoint. Angle is in degrees. 
        #Rotation is counter-clockwise
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

    def findNextSpoilingItem(self):
        """
        Find the item that will expire first from the list of detected products.
        """

        # milliseconds since 01.01.1970 until 01.01.2117
        EXPIRY_DATE_IN_100_YEARS = 4638898800000
        minExpiryDate = EXPIRY_DATE_IN_100_YEARS
        size = self.items.size()
        count = 0 
        minItem = None

        while count < size:
            item = self.items.getItem(count)
            itemExpirationDate = item.expirationDateTimestamp

            if itemExpirationDate < minExpiryDate:
                minExpiryDate = itemExpirationDate
                minItem = self.items.getItem(count)

            count += 1
            # print(count)

        return minItem

    def rotate(self, angle, direction):
        """
        Rotates the plate for <angle> into <direction>
        """

        self.stepperController.turn(angle, direction)

    def getAngle(self,plateCenter,itemCenter):

        dx = itemCenter[0] - plateCenter[0]
        dy = itemCenter[1] - plateCenter[1]

        angle = math.atan2(dy, dx) * 180 / math.pi

        
        return angle
