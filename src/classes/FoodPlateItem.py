import datetime
import iso8601

class FoodPlateItem():
    
    def __init__(self, expirationDate, expirationDateTimestamp, name, positionAngle, center):
        
        self.expirationDate = expirationDate
        self.expirationDateTimestamp = expirationDateTimestamp
        self.name = name
        self.positionAngle = positionAngle
        self.center = center

    def setPositionAngle(self,positionAngle):
        self.positionAngle = positionAngle


    def setCenter(self,center):
        self.center = center

