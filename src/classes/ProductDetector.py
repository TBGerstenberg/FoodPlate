# import the necessary packages
import numpy as np
import cv2
import argparse
from classes.FoodPlate import FoodPlate
from classes.FoodPlateItem import FoodPlateItem

# import the necessary packages


foodPlate = FoodPlate()
class ProductDetector():


    def __init__(self):

        self.imageReadPath = "/home/pi/Projects/FoodPlate/images/raw_input/"
        self.imageWritePath = "/home/pi/Projects/FoodPlate/images/processed_output/"
        self.foundItems = {}
    
    def detectProducts(self, imageToScan):

        #boundaries = [([118, 114, 111], [130, 120, 118])]
    
              
        # load the image
        imageOrig = cv2.imread("/home/pi/Projects/FoodPlate/images/raw_input/input.jpg")
        
        
        # show the images
        cv2.imwrite(self.imageWritePath + "test.jpg", imageOrig)
        
        
        # Crop from x, y, w, h -> 100, 200, 300, 400
        image = imageOrig[0:1080, 275:1670]
        # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]

        height, width, depth = image.shape
        circle_img = np.zeros((height, width), np.uint8)
        cv2.circle(circle_img, (795, 530), 550, 1, thickness=-1)

        masked_data = cv2.bitwise_and(image, image, mask=circle_img)

        cv2.imwrite(self.imageWritePath + "1_masked.jpg", masked_data)

        gray = cv2.cvtColor(masked_data, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        edged = self.auto_canny(blurred)

        cv2.imwrite(self.imageWritePath + "2_edged.jpg", edged)

        # construct and apply a closing kernel to 'close' gaps between 'white'
        # pixels

        kernel = np.ones((1, 8), np.uint8)
        erosion = cv2.dilate(edged, kernel, iterations=2)

        cv2.imwrite(self.imageWritePath + "3_dilated.jpg", erosion)

        kernel2 = np.ones((1, 8), np.uint8)
        erosion2 = cv2.erode(erosion, kernel2, iterations=2)

        cv2.imwrite(self.imageWritePath + "4_eroded.jpg", erosion2)

        kernel4 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 10))
        closed2 = cv2.morphologyEx(erosion2, cv2.MORPH_CLOSE, kernel4)

        cv2.imwrite(self.imageWritePath + "5_closed.jpg", closed2)

        self.findContours(image,closed2)
        self.drawNames(image,closed2)

    def auto_canny(self, image, sigma=0.99):

        # compute the median of the single channel pixel intensities
        v = np.median(image)

        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(image, lower, upper)

        # return the edged image
        return edged

    def findContours(self,original,image):

        (cnts, _) = cv2.findContours(image.copy(),
                                     cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        total = 0

        # loop over the contours
        for c in cnts:

            # finally, get the min enclosing circle
            (x, y), radius = cv2.minEnclosingCircle(c)
            # convert all values to int
            center = (int(x), int(y))

            print "center:" + str(tuple(center))

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(original, '.', (795, 530), font, 1, (255, 255, 255), 2)

            radius = int(radius)

            if radius < 500 and radius > 30:
                # and draw the circle in blue
                cv2.circle(original, center, radius, (255, 0, 0), 2)
                
                total += 1
                self.foundItems["foodPlateItem"+str(total)] = [center,radius]
                
                print("radius:" + str(radius))
            
        self.setFoodPlateItems()



    def drawNames(self,original,image):
    
        (cnts, _) = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        total = 0
        # loop over the contours
        for c in cnts:
            
            # finally, get the min enclosing circle
            (x, y), radius = cv2.minEnclosingCircle(c)
            # convert all values to int
            center = (int(x), int(y))
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            
            radius = int(radius)
            
            if radius < 500 and radius > 30:
                # and draw the circle in blue
                if(total <= foodPlate.items.size()-1):
                    cv2.putText(original, foodPlate.items.getItem(total).name, center, font, 1, (255, 255, 255), 2)
                total += 1
        cv2.imwrite(self.imageWritePath + "final_output.jpg", original)

    def setFoodPlateItems(self):
    
        foodPlateItem1 = FoodPlateItem("2007-01-25T12:00:00Z",1169722800,"Marmelade",0,())
        foodPlateItem2 = FoodPlateItem("2009-05-21T12:00:00Z",1242900000,"Erbsen",0,())
        foodPlateItem3 = FoodPlateItem("2008-02-21T12:00:00Z",1203591600,"Knoblauch",0,())
        foodPlateItem4 = FoodPlateItem("2011-03-10T12:00:00Z",1299754800,"Thunfisch",0,())
        foodPlateItem5 = FoodPlateItem("2012-08-29T12:00:00Z",1346234400,"Majonnaise",0,())
        foodPlateItem6 = FoodPlateItem("2013-04-13T12:00:00Z",1365847200,"Kaffeedose",0,())
        
        for item,value in self.foundItems.items():
            
            eval(item).setPositionAngle(value[1])
            eval(item).setCenter(value[0])
        
        foodPlate.addItem(foodPlateItem1)
        foodPlate.addItem(foodPlateItem2)
        foodPlate.addItem(foodPlateItem3)
        foodPlate.addItem(foodPlateItem4)
        foodPlate.addItem(foodPlateItem5)
        foodPlate.addItem(foodPlateItem6)
        
        print(foodPlate.items.size())
#print(foodPlate.items.getItem(2).__dict__)







