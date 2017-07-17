from classes.StepperController import StepperController
from classes.ProductDetector import ProductDetector
from classes.FoodPlate import FoodPlate
from classes.Camera import Camera

from time import sleep

if __name__ == "__main__":

    """
    Create Default FoodPlate Items
    """
    
    
    print("FoodPlate is now active")

    foodPlate = FoodPlate()
    foodPlate.bringItemToFront()