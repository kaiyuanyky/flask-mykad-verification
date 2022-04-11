import re
import cv2
import json
import numpy as np

from termcolor import colored
from detectors.Landmark import Landmark
from detectors.CompareImage import CompareImage

class FraudDetector(object):
    __mustHaveLandmarks = ['icLogoMatched','mykadLogoMatched','flagMatched','securityChipMatched','coatOfArmsMatched']

    def __init__(self, imgFront, imgRear):
        self.__data = {}
        self.__numValidLandmark = 0
        self.__imgFront = imgFront
        self.__imgRear = imgRear

        self.__threshBlurriness = 25
        self.__threshEachLandmark = 20
        self.__threshLandmarksScore = 50
        self.appendToString("thresholdBlurriness", "{:.2f}".format(self.__threshBlurriness))
        self.appendToString("thresholdEachLandmark", "{:.2f}".format(self.__threshEachLandmark))
        self.appendToString("thresholdLandmarksScore", "{:.2f}".format(self.__threshLandmarksScore))

    def checkBlurriness(self, ratio1, ratio2):
        # Can adjust these values for different results
        size = 50
        thresh = self.__threshBlurriness

        # Convert the images to grayscale
        gray1 = cv2.cvtColor(self.__imgFront, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(self.__imgRear, cv2.COLOR_BGR2GRAY)

        # Apply the blur detector using the FFT
        (mean1, isBlurry1) = self.__detectBlurrinessFFT(gray1, size, ratio1, thresh)
        (mean2, isBlurry2) = self.__detectBlurrinessFFT(gray2, size, ratio2, thresh)
        self.__setBlurrinessCompareImage(mean1, mean2)

        # Add the result to the JSON data list
        self.appendToString("frontImageBlurriness", "{:.2f}".format(mean1))
        self.appendToString("isFrontImageBlurred", bool(isBlurry1))
        self.appendToString("rearImageBlurriness", "{:.2f}".format(mean2))
        self.appendToString("isRearImageBlurred", bool(isBlurry2))

        # For display purpose
        color1 = "red" if isBlurry1 else "green"
        color2 = "red" if isBlurry2 else "green"
        print(colored("isFrontImageBlurred: ","blue"), colored("{} ({:.2f}%)".format(isBlurry1,mean1), color1))
        print(colored("isRearImageBlurred: ","blue"), colored("{} ({:.2f}%)".format(isBlurry2,mean2), color2))

    def __setBlurrinessCompareImage(self, mean1, mean2):
        CompareImage.setOffsetPercent(mean1, mean2)

    def __detectBlurrinessFFT(self, image, size, ratio, thresh):
        # Get the image dimensions, and use the dimensions to derive the center coordinates
        h,w = image.shape
        x,y = (int(w/2.0), int(h/2.0))

        # Compute FFT to find the frequency transform, then shift the zero frequency component
        fft = np.fft.fft2(image)
        fftShift = np.fft.fftshift(fft)

        # Zero out the center of the FFT shift, apply the inverse shift, and then apply the inverse FFT
        fftShift[y-size:y+size, x-size:x+size] = 0
        fftShift = np.fft.ifftshift(fftShift)
        recon = np.fft.ifft2(fftShift)

        # Compute the magnitude spectrum, and the mean of the magnitude values
        magnitude = np.log(np.abs(recon)) * 20
        mean = np.mean(magnitude)

        mean *= ratio

        # The image will be considered as "blurry" if mean <= threshold
        return (mean, mean <= thresh)

    def compareLandmark(self, title, img1, img2, isDisplay):
        ci = CompareImage(title, img1, img2, isDisplay)
        percentage = ci.compare()

        if(percentage > 100):
            percentage = 90

        if(title == 'towersMatched' or title == 'crownMatched' or title == 'malaysiaWordingMatched'):
            thresh = 10
        else:
            thresh = self.__threshEachLandmark
        
        isMatched = (percentage >= thresh)

        if(isMatched):
            self.__numValidLandmark += 1
        
        # Add the result to the JSON data list
        self.appendToString(re.sub('Matched','MatchingPercent',title), "{:.2f}".format(percentage))
        self.appendToString(title, isMatched)

        # Check if the 'must-have landmark' existed
        self.checkLandmarkExixtence(title, percentage)

        # For display purpose
        color = "green" if isMatched else "red"
        print(colored(title + ":", "blue"), colored("{} ({:.2f}%)".format(isMatched, percentage), color))

        # Means landmark exists
        return percentage > 0
    
    def calculateValidLandmarks(self):
        numTotalLandmarks = Landmark.getTotalGenuineNum()
        allLandmarksMatchingPercent = self.__numValidLandmark / numTotalLandmarks * 100

        self.appendToString("allLandmarksScore", "{}/{}".format(self.__numValidLandmark, numTotalLandmarks))
        self.appendToString("allLandmarksMatchingPercent", "{:.2f}".format(allLandmarksMatchingPercent))
        self.appendToString("landmarksScorePassed", allLandmarksMatchingPercent >= self.__threshLandmarksScore)

        print("Total landmark matching: {}/{}".format(self.__numValidLandmark, numTotalLandmarks))
        print("Landmark matching percentage: {}%".format(allLandmarksMatchingPercent))
    
    def checkLandmarkExixtence(self, landmark, percent):
        if((landmark in FraudDetector.__mustHaveLandmarks) and (percent == 0)):
            self.appendToString(re.sub('Matched','Existence',landmark), False)
        else:
            self.appendToString(re.sub('Matched','Existence',landmark), True)

    def appendToString(self, title, val):
        # Append new json data
        self.__data.update({title: val})

    def __str__(self):
        return json.dumps(self.__data)