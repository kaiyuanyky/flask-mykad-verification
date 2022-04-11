import cv2
import json
import pytesseract

from re import search
from termcolor import colored
from detectors.Landmark import Landmark

class RearLandmarkDetector(object):
    def __init__(self, img):
        self.__data = {}
        self.img = img
        self.h = img.shape[0]
        self.w = img.shape[1]

    def setCoordinates(self):
        # Specify the coordinates of rectangle for each landmark
        self.coatOfArms_x1 = int(self.w * 0.02)
        self.coatOfArms_x2 = int(self.w * 0.25)
        self.coatOfArms_y1 = int(self.h * 0.02)
        self.coatOfArms_y2 = int(self.h * 0.30)
        
        self.touchNGo_x1 = int(self.w * 0.04)
        self.touchNGo_x2 = int(self.w * 0.23)
        self.touchNGo_y1 = int(self.h * 0.72)
        self.touchNGo_y2 = int(self.h * 0.96)
        
        self.atm_x1 = int(self.w * 0.19)
        self.atm_x2 = int(self.w * 0.38)
        self.atm_y1 = int(self.h * 0.72)
        self.atm_y2 = int(self.h * 0.96)
        
        self.headDirSign_x1 = int(self.w * 0.33)
        self.headDirSign_x2 = int(self.w * 0.69)
        self.headDirSign_y1 = int(self.h * 0.28)
        self.headDirSign_y2 = int(self.h * 0.70)

        self.icNum_x1 = int(self.w * 0.26)
        self.icNum_x2 = int(self.w * 0.75)
        self.icNum_y1 = int(self.h * 0.65)
        self.icNum_y2 = int(self.h * 0.79)
        
        self.chip_x1 = int(self.w * 0.63)
        self.chip_x2 = int(self.w * 0.82)
        self.chip_y1 = int(self.h * 0.73)
        self.chip_y2 = int(self.h * 0.94)
        
        self.twinTowers_x1 = int(self.w * 0.15)
        self.twinTowers_x2 = int(self.w * 0.41)
        self.twinTowers_y1 = int(self.h * 0.03)
        self.twinTowers_y2 = int(self.h * 0.85)
        
        self.crown_x1 = int(self.w * 0.52)
        self.crown_x2 = int(self.w * 0.98)
        self.crown_y1 = int(self.h * 0.19)
        self.crown_y2 = int(self.h * 0.85)
        
        self.malaysiaWord_x1 = int(self.w * 0.17)
        self.malaysiaWord_x2 = int(self.w * 0.71)
        self.malaysiaWord_y1 = int(self.h * 0.79)
        self.malaysiaWord_y2 = int(self.h * 0.99)

    def drawActualLandmarks(self, bool):
        # Draw the actual landmarks on MyKad
        try:
            self.r1 = Landmark('Coat of Arms Logo', bool[0], False, (self.coatOfArms_x1,self.coatOfArms_y1), (self.coatOfArms_x2,self.coatOfArms_y2), False)
            self.r2 = Landmark('Touch\'nGo Logo', bool[1], False, (self.touchNGo_x1,self.touchNGo_y1), (self.touchNGo_x2,self.touchNGo_y2), False)
            self.r3 = Landmark('ATM Logo', bool[2], False, (self.atm_x1,self.atm_y1), (self.atm_x2,self.atm_y2), False)
            self.r4 = Landmark('Head Directory Signature', bool[3], False, (self.headDirSign_x1,self.headDirSign_y1), (self.headDirSign_x2,self.headDirSign_y2), False)
            self.r5 = Landmark('IC Number', bool[4], False, (self.icNum_x1,self.icNum_y1), (self.icNum_x2,self.icNum_y2), True)
            self.r6 = Landmark('Chip', bool[5], False, (self.chip_x1,self.chip_y1), (self.chip_x2,self.chip_y2), False)
            self.r7 = Landmark('Petronas Twin Towers', bool[6], False, (self.twinTowers_x1,self.twinTowers_y1), (self.twinTowers_x2,self.twinTowers_y2), False)
            self.r8 = Landmark('King\'s Crown', bool[7], False, (self.crown_x1,self.crown_y1), (self.crown_x2,self.crown_y2), False)
            self.r9 = Landmark('Malaysia Wording', bool[8], False, (self.malaysiaWord_x1,self.malaysiaWord_y1), (self.malaysiaWord_x2,self.malaysiaWord_y2), False)            

            if(bool[0]):
                self.r1.setImage(self.coatOfArms)
                cv2.rectangle(self.img,(self.coatOfArms_x1,self.coatOfArms_y1),(self.coatOfArms_x2,self.coatOfArms_y2),(184,114,57),2) # Coat of Arms
            if(bool[1]):
                self.r2.setImage(self.touchNGo)
                cv2.rectangle(self.img,(self.touchNGo_x1,self.touchNGo_y1),(self.touchNGo_x2,self.touchNGo_y2),(78,81,253),2) # Touch n Go
            if(bool[2]):
                self.r3.setImage(self.atm)
                Landmark.setLandmarkNumHasATM()
                cv2.rectangle(self.img,(self.atm_x1,self.atm_y1),(self.atm_x2,self.atm_y2),(252,27,163),2) # ATM
            if(bool[3]):
                self.r4.setImage(self.headDirSign)
                cv2.rectangle(self.img,(self.headDirSign_x1,self.headDirSign_y1),(self.headDirSign_x2,self.headDirSign_y2),(187,92,245),2) # Head Directory Signature
            if(bool[4]):
                self.r5.setImage(self.icNum)
                self.r5.setData(self.icNumString)
                cv2.rectangle(self.img,(self.icNum_x1,self.icNum_y1),(self.icNum_x2,self.icNum_y2),(188,153,195),2)	# IC Number
            if(bool[5]):
                self.r6.setImage(self.chip)
                cv2.rectangle(self.img,(self.chip_x1,self.chip_y1),(self.chip_x2,self.chip_y2),(12,231,64),2)	# Chip
            if(bool[6]):
                self.r7.setImage(self.twinTowers)
                cv2.rectangle(self.img,(self.twinTowers_x1,self.twinTowers_y1),(self.twinTowers_x2,self.twinTowers_y2),(16,192,135),2)	# Petronas Twin Towers
            if(bool[7]):
                self.r8.setImage(self.crown)
                cv2.rectangle(self.img,(self.crown_x1,self.crown_y1),(self.crown_x2,self.crown_y2),(132,128,227),2) # King's Crown
            if(bool[8]):
                self.r9.setImage(self.malaysiaWord)
                cv2.rectangle(self.img,(self.malaysiaWord_x1,self.malaysiaWord_y1),(self.malaysiaWord_x2,self.malaysiaWord_y2),(201,210,88),2)	# Malaysia Wording
        except:
            print("Couldn\'t draw the landmarks. The coordinates of landmarks have not been specified")

    def generateLandmarks(self):
        # Generate the landmarks in gray
        try:
            self.coatOfArms = cv2.cvtColor(self.img[self.coatOfArms_y1:self.coatOfArms_y2,self.coatOfArms_x1:self.coatOfArms_x2].copy(), cv2.COLOR_BGR2GRAY) 
            self.touchNGo = cv2.cvtColor(self.img[self.touchNGo_y1:self.touchNGo_y2,self.touchNGo_x1:self.touchNGo_x2].copy(), cv2.COLOR_BGR2GRAY)
            self.atm = cv2.cvtColor(self.img[self.atm_y1:self.atm_y2,self.atm_x1:self.atm_x2].copy(), cv2.COLOR_BGR2GRAY)
            self.headDirSign = cv2.cvtColor(self.img[self.headDirSign_y1:self.headDirSign_y2,self.headDirSign_x1:self.headDirSign_x2].copy(), cv2.COLOR_BGR2GRAY)
            self.icNum = cv2.cvtColor(self.img[self.icNum_y1:self.icNum_y2,self.icNum_x1:self.icNum_x2].copy(), cv2.COLOR_BGR2GRAY)
            self.chip = cv2.cvtColor(self.img[self.chip_y1:self.chip_y2,self.chip_x1:self.chip_x2].copy(), cv2.COLOR_BGR2GRAY)
            self.twinTowers = cv2.cvtColor(self.img[self.twinTowers_y1:self.twinTowers_y2,self.twinTowers_x1:self.twinTowers_x2].copy(), cv2.COLOR_BGR2GRAY)
            self.crown = cv2.cvtColor(self.img[self.crown_y1:self.crown_y2,self.crown_x1:self.crown_x2].copy(), cv2.COLOR_BGR2GRAY)
            self.malaysiaWord = cv2.cvtColor(self.img[self.malaysiaWord_y1:self.malaysiaWord_y2,self.malaysiaWord_x1:self.malaysiaWord_x2].copy(), cv2.COLOR_BGR2GRAY)
            self.__extractTextFromLandmarks()
        except:
            print("Couldn\'t generate the landmarks. The coordinates of landmarks have not been specified")

    def __sanitizeIcNum(self, val):
        text = search('([0-9]+[-]*)+', val)
        # Return the IC number if it exists and is valid, return -1 if there is no IC number
        return text.group(0) if(text and len(text.group(0)) == 20) else -1

    def getIcNum(self):
        if(self.icNumString == -1):
            return -1
        
        return self.icNumString[0:14]

    def getFullIcNum(self):
        return self.icNumString

    def __extractTextFromLandmarks(self):
        # Set the tesseract path to use 'image_to_string'
        pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'

        self.icNumString = self.__sanitizeIcNum(pytesseract.image_to_string(self.icNum))
        self.appendToString("rearNRIC", self.icNumString)

    def displayData(self):
        print(colored("IC number (Rear Side):","blue"), self.icNumString)

    def appendLandmarkString(self):
        for i in range(0,len(Landmark.rearInstances)):
            self.appendToString(Landmark.rearInstances[i].getLabel(),Landmark.rearInstances[i].getLandmarkData())
    
    def getMyKad(self):
        # Return the final MyKad
        return self.img
    
    def getLandmarks(self):
        # Return the object of this class
        return self

    def appendToString(self, title, val):
        # Append new json data
        self.__data.update({title: val})

    def __str__(self):
        return json.dumps(self.__data)