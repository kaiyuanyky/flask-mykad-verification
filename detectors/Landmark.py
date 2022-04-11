class Landmark(object):
    frontInstances = []
    rearInstances = []

    __idCounter = 0
    __frontIdCounter = 1
    __rearIdCounter = 1
    
    __totalNumCategoryOCR = 0
    __totalNumCategoryPattern = 0
    __numFrontCategoryOCR = 0
    __numFrontCategoryPattern = 0
    __numRearCategoryOCR = 0
    __numRearCategoryPattern = 0

    # Genuine total for Pattern-Type 
    __totalNumGenuineLandmarks = 14

    def __init__(self, name, existence, isFrontSide, point1, point2, isOCRType):
        self.id = Landmark.__idCounter
        self.name = name
        self.existence = existence
        self.side = isFrontSide
        self.point1 = point1
        self.point2 = point2
        self.setType(isOCRType)
        self.__setLabel()
        self.__idIncrement()

        if(existence):
            if(isFrontSide):
                self.__class__.frontInstances.append(self)
            else:
                self.__class__.rearInstances.append(self)
    
    def reset():
        Landmark.frontInstances = []
        Landmark.rearInstances = []
        Landmark.__idCounter = 0
        Landmark.__frontIdCounter = 1
        Landmark.__rearIdCounter = 1
        Landmark.__totalNumCategoryOCR = 0
        Landmark.__totalNumCategoryPattern = 0
        Landmark.__numFrontCategoryOCR = 0
        Landmark.__numFrontCategoryPattern = 0
        Landmark.__numRearCategoryOCR = 0
        Landmark.__numRearCategoryPattern = 0
        Landmark.__totalNumGenuineLandmarks = 14

    def __idIncrement(self):
        Landmark.__idCounter += 1

        if(self.side):
            Landmark.__frontIdCounter += 1
            if(self.existence):
                if(self.type):
                    Landmark.__totalNumCategoryOCR += 1
                    Landmark.__numFrontCategoryOCR += 1
                else:
                    Landmark.__totalNumCategoryPattern += 1
                    Landmark.__numFrontCategoryPattern += 1
        else:
            Landmark.__rearIdCounter += 1
            if(self.existence):
                if(self.type):
                    Landmark.__totalNumCategoryOCR += 1
                    Landmark.__numRearCategoryOCR += 1
                else:
                    Landmark.__totalNumCategoryPattern += 1
                    Landmark.__numRearCategoryPattern += 1

    def getID(self):
        return self.id

    def __setLabel(self):
        self.label = 'f{}'.format(Landmark.__frontIdCounter) if(self.side and type(self.side) is bool) else 'r{}'.format(Landmark.__rearIdCounter)

    def getLabel(self):
        return self.label

    def setName(self, newName):
        self.name = newName

    def getName(self):
        return self.name

    def setSide(self, side):
        self.side = side

    def getSide(self):
        return self.side

    def setPoint1(self, newPoint):
        self.point1 = newPoint

    def getPoint1(self):
        return self.point1

    def setPoint2(self, newPoint):
        self.point2 = newPoint

    def getPoint2(self):
        return self.point2

    def setType(self, newType):
        self.type = newType
        self.__setTypeDesc()

    def getType(self):
        return self.type

    def __setTypeDesc(self):
        self.typeDesc = 'OCR Landmark' if(self.type and type(self.type) is bool) else 'Pattern Landmark'

    def getTypeDesc(self):
        return self.typeDesc

    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data

    def setImage(self, img):
        self.img = img

    def getImage(self):
        return self.img

    def getTotalNumCategoryOCR():
        return Landmark.__totalNumCategoryOCR

    def getTotalNumCategoryPattern():
        return Landmark.__totalNumCategoryPattern

    def getNumFrontCategoryOCR():
        return Landmark.__numFrontCategoryOCR

    def getNumFrontCategoryPattern():
        return Landmark.__numFrontCategoryPattern

    def getNumRearCategoryOCR():
        return Landmark.__numRearCategoryOCR

    def getNumRearCategoryPattern():
        return Landmark.__numRearCategoryPattern

    def getTotalNum():
        return Landmark.__idCounter

    def setLandmarkNumHasATM():
        Landmark.__totalNumGenuineLandmarks = 15

    def getTotalGenuineNum():
        return Landmark.__totalNumGenuineLandmarks

    def getLandmarkData(self):
        data = {
            'name': self.getName(),
            'type': self.getTypeDesc(),
            'point1': self.getPoint1(),
            'point2': self.getPoint2(),
        }
        if(self.type):
            data['extractedData'] = self.getData()

        return data

    def __str__(self):
        string = 'ID: {}, Name: {}, Type: {}, Point1: {}, Point2: {}'.format(self.getLabel(), self.getName(), self.getTypeDesc(), self.getPoint1(), self.getPoint2())
        if(self.type):
            string += ', Data: {}'.format(self.getData())
        return string