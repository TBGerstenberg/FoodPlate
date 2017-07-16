# import the necessary packages
import numpy as np
import cv2
import argparse

# import the necessary packages



class ProductDetector():


    def __init__(self):

        self.imageReadPath = "/home/pi/Projects/FoodPlate/images/raw_input/"
        self.imageWritePath = "/home/pi/Projects/FoodPlate/images/processed_output/"
    
    def detectProducts(self, imageToScan):

        # load the image
        imageOrig = cv2.imread("/home/pi/Projects/FoodPlate/images/raw_input/input.jpg")
        
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

        kernel = np.ones((1, 5), np.uint8)
        erosion = cv2.dilate(edged, kernel, iterations=2)

        cv2.imwrite(self.imageWritePath + "3_dilated.jpg", erosion)

        kernel2 = np.ones((1, 5), np.uint8)
        erosion2 = cv2.erode(erosion, kernel2, iterations=2)

        cv2.imwrite(self.imageWritePath + "4_eroded.jpg", erosion2)

        kernel4 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 10))
        closed2 = cv2.morphologyEx(erosion2, cv2.MORPH_CLOSE, kernel4)

        cv2.imwrite(self.imageWritePath + "5_closed.jpg", closed2)

        self.findContours(image,closed2)

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
            cv2.putText(original, '.', (750, 520), font, 1, (255, 255, 255), 2)

            radius = int(radius)

            if radius < 500 and radius > 30:
                # and draw the circle in blue
                cv2.circle(original, center, radius, (255, 0, 0), 2)
                total += 1
                print("radius:" + str(radius))

            cv2.imwrite(self.imageWritePath + "final_output.jpg", original)
