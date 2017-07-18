# import the necessary packages
import numpy as np
import cv2


# Define font for writing on the final image
font = cv2.FONT_HERSHEY_SIMPLEX

class ProductDetector():
    """
    Class that represents a ProductDetector.
        
    ProductDetector is used to detect products on a plate 
    with image recognition algorithms
    """

    def __init__(self):
        """
        Initialize a ProductDetector.
        """
        self.imageReadPath = "/home/pi/Projects/FoodPlate/images/raw_input/"
        self.imageWritePath = "/home/pi/Projects/FoodPlate/images/processed_output/"
        self.foundItems = []
        self.imageCenter = (810,570)
        self.original = None
        self.processedImage = None
    
    # used to detect products on a given image
    def detectProducts(self, imageToScan):
  
        # Load the image from the camera
        imageOrig = cv2.imread(self.imageReadPath + "input.jpg")
        
        # Set image as class attribute
        self.original = imageOrig

        # Crop image with [y: y + h, x: x + w]
        image = imageOrig[50:1180, 275:1670]
        
        # Get shape from the image
        height, width, depth = image.shape
        
        # Create blacked out image with same width and height as the image
        blacked_image = np.zeros((height, width), np.uint8)
        
        circleMaskPosition = (self.imageCenter[0],self.imageCenter[1]-20)
        circleMaskDimension = self.imageCenter[1]-20
        
        # Define circular shape of areas of the image that should be non-black
        cv2.circle(blacked_image, circleMaskPosition, circleMaskDimension, 1, thickness=-1)

        # Apply circular shape to the image
        masked_image = cv2.bitwise_and(image, image, mask=blacked_image)
        
        # Create masked image
        cv2.imwrite(self.imageWritePath + "1_masked.jpg", masked_image)

        # Grayscale the masked image (for proper edge detection)
        gray = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
        
        # Slightly blur the greyed out image (for proper edge detection)
        blurred = cv2.GaussianBlur(gray, (5,5), 0)
        
        # Apply Canny Edge Detection Algorithm to the blurred image
        edged = self.auto_canny(blurred)

        # Create edged image
        cv2.imwrite(self.imageWritePath + "2_edged.jpg", edged)
        
        # Create blacked out image with same width and height as the edged image
        circle_mask = np.zeros((edged.shape), np.uint8)
        
        # Define circular shape of areas of the image that should be non-black
        # (slightly smaller than previous circular shape for preventing items to melt with other items)
        cv2.circle(circle_mask, circleMaskPosition, circleMaskDimension-20, 1, thickness=-1)
        
        # Apply circular shape to the image
        edged = cv2.bitwise_and(edged, edged, mask=circle_mask)

        # construct and apply a closing kernel to 'close' gaps between 'white'
        # pixels

        # construct a matrix that is used to increase the size of all found lines
        # and apply it to the edged image
        kernel_dilated = np.ones((1, 30), np.uint8)
        dilation = cv2.dilate(edged, kernel_dilated, iterations=3)

        # Create dilated image
        cv2.imwrite(self.imageWritePath + "3_dilated.jpg", dilation)

        # construct a matrix that is used to decrease the size of all found lines
        # and apply it to the dilated image
        kernel_erosion = np.ones((1, 30), np.uint8)
        erosion = cv2.erode(dilation, kernel_erosion, iterations=3)

        # Create eroded image
        cv2.imwrite(self.imageWritePath + "4_eroded.jpg", erosion)

        # construct a matrix that is used to close gaps between white lines in range
        # of the matrix and apply it to the eroded image
        kernel_closed = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 30))
        closed = cv2.morphologyEx(erosion, cv2.MORPH_CLOSE, kernel_closed)

        # Create closed image
        cv2.imwrite(self.imageWritePath + "5_closed.jpg", closed)

        # Call method to draw item ids on the image
        self.drawItemIds(image,closed)
    
        # set closed image as class attribute
        self.processedImage = closed

    # used to compute the lower and upper thresholds for canny edge detection
    # lower sigma: tighter threshold, higher sigma: wider threshold, 0.33 = default value
    def auto_canny(self, image, sigma=0.33):

        # compute the median of the single channel pixel intensities
        v = np.median(image)

        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(image, lower, upper)

        # return the edged image
        return edged
    
    
    # used to sort detected contours on an image with default method "left-to-right"
    def sort_contours(self,cnts):
        
        # construct the list of circles around the contours
        circles = [cv2.minEnclosingCircle(c) for c in cnts]
        
        # sort contours and circles according to given parameters (circles=1, contours=0)
        (cnts, circles) = zip(*sorted(zip(cnts, circles),
                                            key=lambda b:b[1][0], reverse=False))
                                            
        # return the list of sorted contours and circles
        return (cnts, circles)

    # used to draw timestamps on an image
    def draw_timestamp(self,image, center, textToPrint):
        
        # define variables of the center of the timestamp for centering it on a contour
        x = center[0]
        y = center[1]

        # draw the countour number on the image
        cv2.putText(image, textToPrint, (x+170,y), cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, (255, 255, 255), 2)
    
    def outputDemoImage(self,image):
        cv2.imwrite(self.imageWritePath + "demo.jpg", image)
    
    
    # used to draw contours on a given image
    def draw_contour(self,image, c, i):
        
        # compute the center of the contour area
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        
        # draw the countour number on the image
        cv2.putText(image, "#{}".format(i), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, (255, 255, 255), 2)
                    
        # return the image with the contour number drawn on it
        self.processedImage = cv2.imwrite(self.imageWritePath + "final_output.jpg", image)
    
    # used to find contours of a given image
    def drawItemIds(self,original,image):
        
        # find the contours on the image with applied canny edge detection
        (img, cnts, _) = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,
                                          cv2.CHAIN_APPROX_SIMPLE)
        
        
        # sort the contours
        (cnts, boundingBoxes) = self.sort_contours(cnts)
        
        id = 0
        
        # loop over the (now sorted) contours and draw them
        for c in cnts:

            # create circle for the contour
            (x, y), radius = cv2.minEnclosingCircle(c)
            
            center = (int(x), int(y))
            print ("center:" + str(tuple(center)))

            # optional: mark center of the image
            #cv2.putText(original, '.', self.imageCenter, font, 1, (255, 255, 255), 2)
        
            radius = int(radius)
            print("radius:" + str(radius))

            # omit contours that are too big and too small (primarily to omit wrongly detected contours)
            if radius < 350 and radius > 50:
                # draw circle around found valid contours
                cv2.circle(original, center, radius, (255, 0, 0), 2)
                id += 1
                # put found contours inside list
                self.foundItems.append({"identifier":id,"center":center})
                
                # draw ids only on valid contours
                self.draw_contour(original, c, id)
    
        return self.foundItems


