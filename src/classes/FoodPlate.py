from classes.Node import UnorderedList
from Camera import Camera
import math
from classes.ProductDetector import ProductDetector
from classes.FoodPlateItem import FoodPlateItem
from classes.StepperController import StepperController
import random


class FoodPlate():
    """
    Class that represents a FoodPlate.

    Foodplate is a product that will remind
    a consumer to eat the products in his fridge.
    """

    def __init__(self):
        """
        Initialize a Foodplate.

        Calibrates it's center for future calculation
        of FoodPlateItem positions.
        """
        self.camera = Camera()
        self.mostRecentImage = None
        self.items = UnorderedList()
        self.productDetector = ProductDetector()
        self.plateCenter = self.productDetector.imageCenter
        self.stepperController = StepperController()

    def get_item(self, item):
        """Get an item with a specified index."""
        self.items.getItem(item)

    def add_item(self, item):
        """Add an Item to the FoodPlate."""
        self.items.addItem(item)

    def remove_item(self, item):
        """Remove an Item from the FoodPlate."""
        self.remove(item)

    def size(self):
        """Get the number of items currently stored on the FoodPlate."""
        self.items.size()

    def synchronize_foodplateitems(self):
        """
        Mock-Method: Create a set of FoodPlateItems.

        Assign them to the items found on the plate.
        """
        # Create a set of mock-objects that provide the data-source
        products = [{
            "expirationDate": "2012-07-18T12:00:00Z",
            "timestamp": 1342605600,
            "name": "Marmelade"
        }, {
            "expirationDate": "2009-05-21T12:00:00Z",
            "timestamp": 1242900000,
            "name": "Erbsen"
        }, {
            "expirationDate": "2008-02-21T12:00:00Z",
            "timestamp": 1203591600,
            "name": "Champignon"
        }, {
            "expirationDate": "2007-01-25T12:00:00Z",
            "timestamp": 1169722800,
            "name": "Thunfisch"
        }, {
            "expirationDate": "2013-04-13T12:00:00Z",
            "timestamp": 1365847200,
            "name": "GoetterSpeise"
        }, {
            "expirationDate": "2011-03-10T12:00:00Z",
            "timestamp": 1299754800,
            "name": "Honig"
        }, {
            "expirationDate": "2011-02-13T12:00:00Z",
            "timestamp": 1297594800,
            "name": "Pfeffer"
        }]

        # shuffle raw data for demo purposes, the plate will now assign
        # expiration dates randomly and turn the
        # item that will spoil next to the front
        random.shuffle(products)

        # generate a debug image
        output_image = self.productDetector.original

        # for each item that has been found, create a FoodPlateItem-Object
        count = 0
        for item in self.productDetector.foundItems:

            foodplateitem = FoodPlateItem()
            foodplateitem.identifier = item.get('identifier')
            foodplateitem.center = item.get('center')
            foodplateitem.positionAngle = self.get_angle(
                self.plateCenter, foodplateitem.center)
            foodplateitem.name = products[count].get('name')
            foodplateitem.expirationDate = products[count].get(
                'expirationDate')
            foodplateitem.expirationDateTimestamp = products[count].get(
                'timestamp')
            count += 1
            self.add_item(foodplateitem)
            print(foodplateitem.name + " with id : " +
                  str(foodplateitem.identifier) + " is at: " +
                  str(foodplateitem.positionAngle) + " degrees.")
            self.productDetector.draw_timestamp(
                output_image, foodplateitem.center,
                foodplateitem.expirationDate.split("T")[0])

        # write demo-output image
        self.productDetector.outputDemoImage(output_image)

    def bring_item_to_front(self):
        """
        Turn an Item on the FoodPlate to the front.

        So that it faces a towards a person
        opening a the fridge.
        """
        # detect all items on the plate
        self.scan_items()

        # find the one that expires first
        item_with_earliest_expiry = self.find_next_spoiling_item()

        # if an item could be found
        if (item_with_earliest_expiry is not None):

            print("Item with min expiry date: " +
                  item_with_earliest_expiry.name)

            # calculate where the item is positioned on the plate
            angle = item_with_earliest_expiry.positionAngle

            # 0 degrees is defined at the center of the plate
            # the desired position of the items is at
            turn_angle = 0
            turn_direction = None

            if angle >= 0 and angle <= 180:
                if angle > 90:
                    turn_angle = angle - 90
                    turn_direction = "L"
                elif angle <= 90:
                    turn_angle = 90 - angle
                    turn_direction = "R"

            elif angle < 0 and angle > -180:
                turn_angle = math.fabs(angle) + 90
                turn_direction = "R"

            print(item_with_earliest_expiry.name + " will turn " +
                  str(turn_angle) + " Degrees \n")

            self.rotate(turn_angle, turn_direction)

            print("Angle between plate center and " +
                  item_with_earliest_expiry.name + " is: " + str(angle))

        else:
            print("No Items found")

    def scan_items(self):
        """Take an image and searches for products on the plate."""
        # take image of the plate
        most_recent_image = self.camera.capture_image(
            '/home/pi/Projects/FoodPlate/images/raw_input/input.jpg')

        # detect items on the plate
        self.productDetector.detectProducts(most_recent_image)

        # Fill item list
        self.synchronize_foodplateitems()

    def update_items(self, angle):
        """
        Update the positions of all items after a rotation of <angle> DEG.

        Recalculate the centers of each plateitem after applying a rotation.
        """
        # iterate over all items that are saved
        for item in self.items:

            # update item coordinate after a rotation of <angle> degrees
            item.coordinates = self.rotate_point_2d(self.center, item.center,
                                                    angle)

            # update position measured in DEG
            item.position = item.position + angle

    def rotate_point_2d(self, centerPoint, point, angle):
        """
        Rotate a point around a given center in 2D space.

        Rotation is counter-clockwise.
        """

        angle = math.radians(angle)

        # Move to origin
        temp_point = point[0] - centerPoint[0], point[1] - centerPoint[1]

        # Multiply with 2D rotation matrix
        temp_point = (
            temp_point[0] * math.cos(angle) - temp_point[1] * math.sin(angle),
            temp_point[0] * math.sin(angle) + temp_point[1] * math.cos(angle))

        # move back
        temp_point = temp_point[0] + centerPoint[0], temp_point[1] + centerPoint[1]

        return temp_point

    def find_next_spoiling_item(self):
        """
        Find the item that will expire next from list of detected products.

        Note: This doesnt search correctly for items with
        expiry date after 01.01.2117.
        """
        # milliseconds since 01.01.1970 until 01.01.2117
        expiry_date_in_100_years = 4638898800000
        min_expiry_date = expiry_date_in_100_years
        size = self.items.size()
        count = 0
        min_item = None

        while count < size:
            item = self.items.getItem(count)
            item_expiration_date = item.expirationDateTimestamp

            if item_expiration_date < min_expiry_date:
                min_expiry_date = item_expiration_date
                min_item = self.items.getItem(count)

            count += 1

        return min_item

    def rotate(self, angle, direction):
        """Rotate the plate for <angle> into <direction>."""
        self.stepperController.turn(angle, direction)

    def get_angle(self, plateCenter, itemCenter):
        """
        Calculate the angle between an item on the plate
        and the plate's center.
        """
        dx = itemCenter[0] - plateCenter[0]
        dy = itemCenter[1] - plateCenter[1]

        angle = math.atan2(dy, dx) * 180 / math.pi

        return angle
