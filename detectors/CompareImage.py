import re
import cv2
import numpy as np

class CompareImage(object):
    __ratio = 0.65
    __frontBlurriness = ''
    __rearBlurriness = ''

    __threshEachMatch = {
        # Front
        'icLogo': 200,
        'mykadLogo': 80,
        'flag': 80,
        'mscLogo': 30,
        'securityChip': 70,
        'hibiscus': 40,
        'microprint': 80,
        # Rear
        'coatOfArms': 30,
        'tng': 60,
        'atm': 40,
        'singature': 50,
        'chip': 20,
        'towers': 45,
        'crown': 65,
        'malaysiaWording': 10,
    }

    def __init__(self, title, img1, img2, isDisplay):
        self.title = title
        self.img1 = img1
        self.img2 = img2
        self.isDisplay = isDisplay

    def compare(self):
        numQualityPoints = self.getQualityPoints()
        thresh = self.__getThresh(re.sub('Matched', '', self.title))

        # Return 0 indicates that the landmark does not match
        return (numQualityPoints/thresh * 100) if (numQualityPoints > 0) else 0

    def getQualityPoints(self):
        sift = cv2.SIFT_create()
        keyPoint1, desc1 = sift.detectAndCompute(self.img1, None)
        keyPoint2, desc2 = sift.detectAndCompute(self.img2, None)

        searchParams = dict()
        indexParams = dict(algorithm=0, trees=5)
        matches = cv2.FlannBasedMatcher(indexParams, searchParams).knnMatch(desc1, desc2, k=2)
        
        # Lower ratio may result in high quality matches, but may get only few matches
        ratio = 0.8
        qualityPoints = []
        
        for m,n in matches:
            if m.distance < (n.distance * ratio):
                qualityPoints.append(m)

        # If true, display the compared landmarks
        if self.isDisplay:
            # Draw matches of comparison on the images
            output = cv2.drawMatches(self.img1, keyPoint1, self.img2, keyPoint2, qualityPoints, None)
            cv2.imshow(self.title, output)

        # Return the number of matching quality points
        return len(qualityPoints)

    def __getThresh(self, landmark):
        return CompareImage.__threshEachMatch[landmark]

    def setOffsetPercent(frontBlurriness, rearBlurriness):
        CompareImage.__frontBlurriness = float(np.round(frontBlurriness/100, 2))
        CompareImage.__rearBlurriness = float(np.round(rearBlurriness/100, 2))