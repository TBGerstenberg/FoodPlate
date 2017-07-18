

class FoodPlateItem():
    """
    Class that represents an item that can be positioned on a foodplate.
    """
    def __init__(self, expirationDate="1970-07-18T12:00:00Z", expirationDateTimestamp = 1342605600, name = "NOT_SET", positionAngle = None, center = None, identifier = None):
        
        self.expirationDate = expirationDate
        self.expirationDateTimestamp = expirationDateTimestamp
        self.name = name
        self.positionAngle = positionAngle
        self.center = center
        self.identifier = identifier
    
    def setPositionAngle(self,positionAngle):
        self.positionAngle = positionAngle
    
    
    def setCenter(self,center):
        self.center = center
    
    def getName(self):
        return self.name
