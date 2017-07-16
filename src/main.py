from classes.StepperController import StepperController
from classes.FoodPlateItem import FoodPlateItem
from classes.ProductDetector import ProductDetector
from classes.Camera import Camera

from time import sleep

if __name__ == "__main__":

    """
    Create Default FoodPlate Items
    """
    
    
    print("FoodPlate is now active")

    camera = Camera()
    image = camera.takeImage()

    print("Initial image taken")
    
    productDetector = ProductDetector()
    productDetector.detectProducts(image)



    #sp = StepperController()
    #sp.turn(90, "L")
