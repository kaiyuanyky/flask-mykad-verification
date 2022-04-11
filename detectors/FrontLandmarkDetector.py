import re
import cv2
import json
import imutils
import datetime
import pytesseract

from re import search
from datetime import date
from termcolor import colored
from detectors.Landmark import Landmark

class FrontLandmarkDetector(object):
    def __init__(self, img):
        self.__data = {}
        self.img = img
        self.h = img.shape[0]
        self.w = img.shape[1]

    def setCoordinates(self):
        # Specify the coordinates of rectangle for each landmark
        self.icLogo_x1 = int(self.w * 0.01)
        self.icLogo_x2 = int(self.w * 0.60)
        self.icLogo_y1 = int(self.h * 0.001)
        self.icLogo_y2 = int(self.h * 0.26)
        
        self.myKadLogo_x1 = int(self.w * 0.56)
        self.myKadLogo_x2 = int(self.w * 0.76)
        self.myKadLogo_y1 = int(self.h * 0.001)
        self.myKadLogo_y2 = int(self.h * 0.28)
        
        self.malaysiaFlag_x1 = int(self.w * 0.71)
        self.malaysiaFlag_x2 = int(self.w * 0.99)
        self.malaysiaFlag_y1 = int(self.h * 0.001)
        self.malaysiaFlag_y2 = int(self.h * 0.28)
        
        self.mscLogo_x1 = int(self.w * 0.25)
        self.mscLogo_x2 = int(self.w * 0.69)
        self.mscLogo_y1 = int(self.h * 0.14)
        self.mscLogo_y2 = int(self.h * 0.52)
        
        self.icNum_x1 = int(self.w * 0.03)
        self.icNum_x2 = int(self.w * 0.38)
        self.icNum_y1 = int(self.h * 0.19)
        self.icNum_y2 = int(self.h * 0.31)
        
        self.securityChip_x1 = int(self.w * 0.03)
        self.securityChip_x2 = int(self.w * 0.30)
        self.securityChip_y1 = int(self.h * 0.26)
        self.securityChip_y2 = int(self.h * 0.61)
        
        self.name_x1 = int(self.w * 0.01)
        self.name_x2 = int(self.w * 0.63)
        self.name_y1 = int(self.h * 0.61)
        self.name_y2 = int(self.h * 0.75)
        
        self.address_x1 = int(self.w * 0.01)
        self.address_x2 = int(self.w * 0.51)
        self.address_y1 = int(self.h * 0.73)
        self.address_y2 = int(self.h * 0.98)
        
        self.citizen_x1 = int(self.w * 0.62)
        self.citizen_x2 = int(self.w * 0.99)
        self.citizen_y1 = int(self.h * 0.84)
        self.citizen_y2 = int(self.h * 0.99)
        
        self.hibiscus_x1 = int(self.w * 0.39)
        self.hibiscus_x2 = int(self.w * 0.81)
        self.hibiscus_y1 = int(self.h * 0.67)
        self.hibiscus_y2 = int(self.h * 0.999)
        
        self.microprint_x1 = int(self.w * 0.28)
        self.microprint_x2 = int(self.w * 0.58)
        self.microprint_y1 = int(self.h * 0.58)
        self.microprint_y2 = int(self.h * 0.96)

    def __drawFaces(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.faces = face_cascade.detectMultiScale(img_gray, 1.1, 4)
        for (x,y,w,h) in self.faces:
            self.img = cv2.rectangle(self.img, (x,y), (x+w,y+h), (255,0,0), 2)
            roi_gray = img_gray[y:y+h, x:x+w]
            roi_color = self.img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 3)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh), (0,255,0),2)

    def getFaces(self):
        return self.faces

    def drawLandmarks(self):
        # Draw the face landmark on MyKad
        self.__drawFaces()

    def drawActualLandmarks(self, bool):
        # Draw the actual landmarks on MyKad
        try:
            self.f1 = Landmark('IC Logo', bool[0], True, (self.icLogo_x1,self.icLogo_y1), (self.icLogo_x2,self.icLogo_y2), False)
            self.f2 = Landmark('MyKad Logo', bool[1], True, (self.myKadLogo_x1,self.myKadLogo_y1), (self.myKadLogo_x2,self.myKadLogo_y2), False)
            self.f3 = Landmark('Malaysia Flag', bool[2], True, (self.malaysiaFlag_x1,self.malaysiaFlag_y1), (self.malaysiaFlag_x2,self.malaysiaFlag_y2), False)
            self.f4 = Landmark('MSC Logo', bool[3], True, (self.mscLogo_x1,self.mscLogo_y1), (self.mscLogo_x2,self.mscLogo_y2), False)
            self.f5 = Landmark('IC Number', bool[4], True, (self.icNum_x1,self.icNum_y1), (self.icNum_x2,self.icNum_y2), True)
            self.f6 = Landmark('Security Chip', bool[5], True, (self.securityChip_x1,self.securityChip_y1), (self.securityChip_x2,self.securityChip_y2), False)
            self.f7 = Landmark('Name', bool[6], True, (self.name_x1,self.name_y1), (self.name_x2,self.name_y2), True)
            self.f8 = Landmark('Address', bool[7], True, (self.address_x1,self.address_y1), (self.address_x2,self.address_y2), True)
            self.f9 = Landmark('Citizenship', bool[8], True, (self.citizen_x1,self.citizen_y1), (self.citizen_x2,self.citizen_y2), True)
            self.f10 = Landmark('Hibiscus Logo', bool[9], True, (self.hibiscus_x1,self.hibiscus_y1), (self.hibiscus_x2,self.hibiscus_y2), False)
            self.f11 = Landmark('Microprint', bool[10], True, (self.microprint_x1,self.microprint_y1), (self.microprint_x2,self.microprint_y2), False)

            if(bool[0]):    
                self.f1.setImage(self.icLogo)
                cv2.rectangle(self.img,(self.icLogo_x1,self.icLogo_y1),(self.icLogo_x2,self.icLogo_y2),(184,114,57),2) # IC Logo
            if(bool[1]):
                self.f2.setImage(self.myKadLogo)
                cv2.rectangle(self.img,(self.myKadLogo_x1,self.myKadLogo_y1),(self.myKadLogo_x2,self.myKadLogo_y2),(99,187,93),2) # MyKad Logo
            if(bool[2]):
                self.f3.setImage(self.malaysiaFlag)
                cv2.rectangle(self.img,(self.malaysiaFlag_x1,self.malaysiaFlag_y1),(self.malaysiaFlag_x2,self.malaysiaFlag_y2),(78,81,253),2) # Malaysia Flag
            if(bool[3]):
                self.f4.setImage(self.mscLogo)
                cv2.rectangle(self.img,(self.mscLogo_x1,self.mscLogo_y1),(self.mscLogo_x2,self.mscLogo_y2),(252,27,163),2) # MSC Logo
            if(bool[4]):
                self.f5.setImage(self.icNum)
                self.f5.setData([self.getIcNum(), self.getGender(), self.getAge()])
                cv2.rectangle(self.img,(self.icNum_x1,self.icNum_y1),(self.icNum_x2,self.icNum_y2),(187,92,245),2) # IC Number
            if(bool[5]):
                self.f6.setImage(self.securityChip)
                cv2.rectangle(self.img,(self.securityChip_x1,self.securityChip_y1),(self.securityChip_x2,self.securityChip_y2),(188,153,195),2)	# Security Chip
            if(bool[6]):
                self.f7.setImage(self.name)
                self.f7.setData(self.getName())
                cv2.rectangle(self.img,(self.name_x1,self.name_y1),(self.name_x2,self.name_y2),(12,231,64),2)	# Name
            if(bool[7]):
                self.f8.setImage(self.address)
                self.f8.setData(self.getAddress())
                cv2.rectangle(self.img,(self.address_x1,self.address_y1),(self.address_x2,self.address_y2),(16,192,135),2)	# Address
            if(bool[8]):
                self.f9.setImage(self.citizen)
                self.f9.setData(self.getCitizen())
                cv2.rectangle(self.img,(self.citizen_x1,self.citizen_y1),(self.citizen_x2,self.citizen_y2),(132,128,227),2)	# Citizen
            if(bool[9]):
                self.f10.setImage(self.hibiscus)
                cv2.rectangle(self.img,(self.hibiscus_x1,self.hibiscus_y1),(self.hibiscus_x2,self.hibiscus_y2),(201,210,88),2)	# Hibiscus image
            if(bool[10]):
                self.f11.setImage(self.microprint)
                cv2.rectangle(self.img,(self.microprint_x1,self.microprint_y1),(self.microprint_x2,self.microprint_y2),(182,194,149),2)	# Microprint
        except:
            print("Couldn\'t draw the landmarks. The coordinates of landmarks have not been set")

    def generateLandmarks(self):
        # Generate the landmarks in gray
        try:
            self.icLogo = cv2.cvtColor(self.img[self.icLogo_y1:self.icLogo_y2,self.icLogo_x1:self.icLogo_x2].copy(), cv2.COLOR_BGR2GRAY) 
            self.myKadLogo = cv2.cvtColor(self.img[self.myKadLogo_y1:self.myKadLogo_y2,self.myKadLogo_x1:self.myKadLogo_x2].copy(), cv2.COLOR_BGR2GRAY)
            self.malaysiaFlag = cv2.cvtColor(self.img[self.malaysiaFlag_y1:self.malaysiaFlag_y2,self.malaysiaFlag_x1:self.malaysiaFlag_x2].copy(), cv2.COLOR_BGR2GRAY)
            self.mscLogo = cv2.cvtColor(self.img[self.mscLogo_y1:self.mscLogo_y2,self.mscLogo_x1:self.mscLogo_x2].copy(), cv2.COLOR_BGR2GRAY)
            self.icNum = cv2.cvtColor(self.img[self.icNum_y1:self.icNum_y2,self.icNum_x1:self.icNum_x2].copy(), cv2.COLOR_BGR2GRAY)
            self.securityChip = cv2.cvtColor(self.img[self.securityChip_y1:self.securityChip_y2,self.securityChip_x1:self.securityChip_x2].copy(), cv2.COLOR_BGR2GRAY)
            self.name = cv2.cvtColor(self.img[self.name_y1:self.name_y2, self.name_x1:self.name_x2].copy(), cv2.COLOR_BGR2GRAY)
            self.address = cv2.cvtColor(self.img[self.address_y1:self.address_y2,self.address_x1:self.address_x2].copy(), cv2.COLOR_BGR2GRAY)
            self.citizen = cv2.cvtColor(self.img[self.citizen_y1:self.citizen_y2,self.citizen_x1:self.citizen_x2].copy(), cv2.COLOR_BGR2GRAY)
            self.hibiscus = cv2.cvtColor(self.img[self.hibiscus_y1:self.hibiscus_y2,self.hibiscus_x1:self.hibiscus_x2].copy(), cv2.COLOR_BGR2GRAY)
            self.microprint = cv2.cvtColor(self.img[self.microprint_y1:self.microprint_y2,self.microprint_x1:self.microprint_x2].copy(), cv2.COLOR_BGR2GRAY)
            self.__extractTextFromLandmarks()
        except:
            print("Couldn\'t generate the landmarks. The coordinates of landmarks have not been set")

    def getName(self):
        return self.nameString

    def getIcNum(self):
        return self.icNumString

    def getGender(self):
        if(self.icNumString == -1):
            return -1

        # Return Female if the last digit of IC number is even, else return Male (odd)
        return "Female" if(int(self.icNumString[-1]) % 2 == 0) else "Male"

    def getAge(self):
        try:
            day = self.icNumString[4:6]
            month = self.icNumString[2:4]
            year = self.icNumString[0:2]
            
            if(self.icNumString[0] != '0'):
                year = "19" + year 
            else:
                year = "20" + year

            birthDate = datetime.date(int(year),int(month),int(day))
            age = date.today() - birthDate

            # Convert the age from days to years
            return int(age.days / 365)
        except:
            # Invalid NRIC detected
            return -1

    def getAddress(self):
        return self.__beautifyAddress(self.addressString)

    def getCitizen(self):
        return self.__beautifyCitizen(self.citizenString)

    def __sanitizeIcNum(self, val):
        text = search('([0-9]+[-]*)+', val)
        # Return the IC number if it exists and is valid, return -1 if there is no IC number
        return text.group(0) if(text and len(text.group(0)) == 14) else -1

    def __sanitizeName(self, val):
        # Substitute those \s (\t\n\r\f\v) with whitespace, and then remove the whitespace at the end (rstrip())
        return re.sub('\s+',' ',val).rstrip()

    def __sanitizeAddress(self, val):
        val = val.strip()

        # Remove additional/redundant nextline character from the address
        for i in range(len(val)):
            if(i < len(val)-1):
                if(val[i] == "\n" and val[i+1] == "\n"):
                    val = val[0:i] + val[i+1::]
        return val

    def __beautifyAddress(self, val):
        # Substitute the nextline character with comma
        val = re.sub('\n+',', ',val)
        # Substitute those \s (\t\n\r\f\v) characters with whitespace so that the address become one line
        val = re.sub('\s+',' ',val)
        return val

    def __beautifyCitizen(self, val):
        try:
            return val[val.index('W'):].lstrip()
        except ValueError:
            return val

    def __preprocessImageOCR(self, val, width, kernel):
        # Preprocess the image needed for OCR so that the image's background is all displayed 
        # in white, and the text is clearly displayed in black for a better recognition

        image = imutils.resize(val, width=width)

        se = cv2.getStructuringElement(cv2.MORPH_RECT, kernel)
        bg = cv2.morphologyEx(image, cv2.MORPH_DILATE, se)

        outputGray = cv2.divide(image, bg, scale=255)
        outputBinary = cv2.threshold(outputGray, 0, 255, cv2.THRESH_OTSU)[1]

        return outputBinary

    def __extractTextFromLandmarks(self):
        # Set the tesseract path to use 'image_to_string'
        pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'

        # Set different configuration modes for different OCR landmark
        # FIXME
        icNumConfig = '--psm 4 outputbase digits'
        nameConfig = '--psm 7'
        addressConfig = '--psm 6 -c tessedit_char_blacklist={}$:,'
        citizenConfig = '--psm 6 -c tessedit_char_whitelist=AEGHIKLMNPRSUW'

        # FIXME
        icNumWidth = 250
        nameWidth = 350
        addressWidth = 280
        citizenWidth = 280

        # FIXME
        icNumKernel = (4,8)
        nameKernel = (4,8)
        addressKernel = (3,6)
        citizenKernel = (3,6)

        self.icNumString = self.__sanitizeIcNum(pytesseract.image_to_string(self.__preprocessImageOCR(self.icNum,icNumWidth,icNumKernel),config=icNumConfig))
        self.nameString = self.__sanitizeName(pytesseract.image_to_string(self.__preprocessImageOCR(self.name,nameWidth,nameKernel),config=nameConfig))
        self.addressString = self.__sanitizeAddress(pytesseract.image_to_string(self.__preprocessImageOCR(self.address,addressWidth,addressKernel),config=addressConfig))
        self.citizenString = self.__sanitizeName(pytesseract.image_to_string(self.__preprocessImageOCR(self.citizen,citizenWidth,citizenKernel),config=citizenConfig))

        self.appendToString("frontNRIC", self.getIcNum())
        self.appendToString("name", self.getName())
        self.appendToString("gender", self.getGender())
        self.appendToString("age", self.getAge())
        self.appendToString("address", self.getAddress())
        self.appendToString("citizen", self.getCitizen())

    def displayData(self):
        print(colored("IC number (Front Side):","blue"), self.getIcNum())
        print(colored("Name:","blue"), self.getName())
        print(colored("Gender:","blue"), self.getGender())
        print(colored("Age:","blue"), self.getAge())
        print(colored("Address:","blue"), self.getAddress())
        print(colored("Citizen:","blue"), self.getCitizen())

    def appendLandmarkString(self):
        for i in range(0,len(Landmark.frontInstances)):
            self.appendToString(Landmark.frontInstances[i].getLabel(), Landmark.frontInstances[i].getLandmarkData())
    
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