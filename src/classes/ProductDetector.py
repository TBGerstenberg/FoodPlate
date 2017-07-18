# import the necessary packages
import numpy as np
import cv2
import argparse

# import the necessary packages

class ProductDetector():


    def __init__(self):

        self.imageReadPath = "/home/pi/Projects/FoodPlate/images/raw_input/"
        self.imageWritePath = "/home/pi/Projects/FoodPlate/images/processed_output/"
        self.foundItems = []
        self.imageCenter = (810,570)
        self.original = None
        self.processedImage = None
    
    def detectProducts(self, imageToScan):

        #boundaries = [([118, 114, 111], [130, 120, 118])]
    
              
        # load the image
        imageOrig = cv2.imread("/home/pi/Projects/FoodPlate/images/raw_input/input.jpg")
        
        self.original = imageOrig
        
        # show the images
        
        
        # Crop from x, y, w, h -> 100, 200, 300, 400
        image = imageOrig[50:1180, 275:1670]
        # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
        
        height, width, depth = image.shape
        
        circle_img = np.zeros((height, width), np.uint8)
        
        
        circleMaskPosition = (self.imageCenter[0],self.imageCenter[1]-20)
        circleMaskDimension = self.imageCenter[1]-20
        
        cv2.circle(circle_img, circleMaskPosition, circleMaskDimension, 1, thickness=-1)
       
        masked_data = cv2.bitwise_and(image, image, mask=circle_img)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.rectangle(masked_data, (1350,410), (1297,620), (0,0,0), -1, 8, 0)
        #cv2.putText(masked_data, '.', (825,550), font, 1, (255, 255, 255), 2)

        cv2.imwrite(self.imageWritePath + "1_masked.jpg", masked_data)

        gray = cv2.cvtColor(masked_data, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5,5), 0)
        edged = self.auto_canny(blurred)

        cv2.imwrite(self.imageWritePath + "2_edged.jpg", edged)
        
        circle_mask = np.zeros((edged.shape), np.uint8)
        
        cv2.circle(circle_mask, circleMaskPosition, circleMaskDimension-20, 1, thickness=-1)
        
        edged = cv2.bitwise_and(edged, edged, mask=circle_mask)

        # construct and apply a closing kernel to 'close' gaps between 'white'
        # pixels

        kernel = np.ones((1, 30), np.uint8)
        erosion = cv2.dilate(edged, kernel, iterations=3)

        cv2.imwrite(self.imageWritePath + "3_dilated.jpg", erosion)

        kernel2 = np.ones((1, 30), np.uint8)
        erosion2 = cv2.erode(erosion, kernel2, iterations=3)

        cv2.imwrite(self.imageWritePath + "4_eroded.jpg", erosion2)

        kernel4 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 30))
        closed2 = cv2.morphologyEx(erosion2, cv2.MORPH_CLOSE, kernel4)

        cv2.imwrite(self.imageWritePath + "5_closed.jpg", closed2)

        self.drawItemIds(image,closed2)
    
        self.processedImage = closed2

    def auto_canny(self, image, sigma=0.33):

        # compute the median of the single channel pixel intensities
        v = np.median(image)

        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(image, lower, upper)

        # return the edged image
        return edged
    
    def sort_contours(self,cnts, method="left-to-right"):
        # initialize the reverse flag and sort index
        # construct the list of bounding boxes and sort them from top to
        # bottom
        
        boundingBoxes = [cv2.minEnclosingCircle(c) for c in cnts]
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                            key=lambda b:b[1][0], reverse=False))
                                            
                                            # return the list of sorted contours and bounding boxes
        return (cnts, boundingBoxes)

    
    def draw_timestamp(self,image, center, textToPrint):
        
        x = center[0]
        y = center[1]

        # draw the countour number on the image
        cv2.putText(image, textToPrint, (x+170,y), cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, (255, 255, 255), 2)
    
    def outputDemoImage(self,image):
        cv2.imwrite(self.imageWritePath + "demo.jpg", image)
    
    def draw_contour(self,image, c, i):
        # compute the center of the contour area and draw a circle
        # representing the center
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        
        # draw the countour number on the image
        cv2.putText(image, "#{}".format(i), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, (255, 255, 255), 2)
                    
                    # return the image with the contour number drawn on it
                    
        self.processedImage = cv2.imwrite(self.imageWritePath + "final_output.jpg", image)
    
    
    
    
    def drawItemIds(self,original,image):
        
        (cnts, _) = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,
                                          cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
                                          
        # sort the contours according to the provided method
        (cnts, boundingBoxes) = self.sort_contours(cnts, "left-to-right")
                                          
        # loop over the (now sorted) contours and draw them
                                          
        id = 0
                                          
        for c in cnts:

            (x, y), radius = cv2.minEnclosingCircle(c)
            # convert all values to int
            center = (int(x), int(y))

            print ("center:" + str(tuple(center)))

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(original, '.', self.imageCenter, font, 1, (255, 255, 255), 2)
        
            radius = int(radius)

            print("radius:" + str(radius))

            if radius < 350 and radius > 50:
                cv2.circle(original, center, radius, (255, 0, 0), 2)
                id += 1
                self.foundItems.append({"identifier":id,"center":center})
                self.draw_contour(original, c, id)
        return self.foundItems


