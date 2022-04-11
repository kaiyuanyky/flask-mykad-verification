import io
import os
import cv2
import flask
import imutils
import base64
import numpy as np
import pandas as pd

from PIL import Image
from imageio import imread
from io import BufferedReader

from detectors.Landmark import Landmark
from detectors.ShapeDetector import ShapeDetector
from detectors.FraudDetector import FraudDetector
from detectors.FrontLandmarkDetector import FrontLandmarkDetector
from detectors.RearLandmarkDetector import RearLandmarkDetector

from flask import Flask, redirect, jsonify, json, render_template, request, send_file

app = Flask(__name__)

fld = ""
rld = ""
fd = ""

front_img = ""
front_img_resized = ""
front_img_ratio = ""
front_img_gray = ""
front_img_blurred = ""
front_img_thresh = ""
front_img_cropped = ""

rear_img = ""
rear_img_resized = ""
rear_img_ratio = ""
rear_img_gray = ""
rear_img_blurred = ""
rear_img_thresh = ""
rear_img_cropped = ""

def init(front, rear):
    global front_img
    global front_img_resized
    global front_img_ratio
    global front_img_gray
    global front_img_blurred
    global front_img_thresh

    global rear_img
    global rear_img_resized
    global rear_img_ratio
    global rear_img_gray
    global rear_img_blurred
    global rear_img_thresh

    # Load the image and resize it to a smaller factor so that the shapes can be approximated better
    front_img = front
    front_img_resized = imutils.resize(front_img, width=500)
    front_img_ratio = front_img.shape[0] / float(front_img_resized.shape[0])
    rear_img = rear
    rear_img_resized = imutils.resize(rear_img, width=500)
    rear_img_ratio = rear_img.shape[0] / float(rear_img_resized.shape[0])

    # Convert the resized image to grayscale, blur it slightly, and threshold it
    front_img_gray = cv2.cvtColor(front_img_resized, cv2.COLOR_BGR2GRAY)
    front_img_blurred = cv2.GaussianBlur(front_img_gray, (5, 5), 0)
    front_img_thresh = cv2.threshold(front_img_blurred, 60, 255, cv2.THRESH_BINARY)[1]
    rear_img_gray = cv2.cvtColor(rear_img_resized, cv2.COLOR_BGR2GRAY)
    rear_img_blurred = cv2.GaussianBlur(rear_img_gray, (5, 5), 0)
    rear_img_thresh = cv2.threshold(rear_img_blurred, 60, 255, cv2.THRESH_BINARY)[1]

def preprocessImage(img, thresh, ratio, resized):
    # Find the contours in the thresholded image and initialize the shape detector
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    sd = ShapeDetector()

    # Initialize the largest values
    largest = 0
    largestCountour = contours[0]

    # Loop over the contours
    for c in contours:
        # Compute the center of the contour, then detect the name of the shape using only the contour
        M = cv2.moments(c)
    
        # Id m00 is 0, set it to 1 to avoid ZeroDivisionError later on
        m00 = 1.0 if(M["m00"] == 0.0) else M["m00"]

        cX = int((M["m10"] / m00) * ratio)
        cY = int((M["m01"] / m00) * ratio)
        shape = sd.detect(c)

        # If the shape is rectangle, then store the largest one
        if shape == "rectangle":
            area = cv2.contourArea(c)
            if area > largest:
                largest = area
                largestCountour = c
                x,y,w,h = cv2.boundingRect(c)
                img_cropped = resized[y:y+h, x:x+w]

    # Resize the cropped image back to standard size of width=500
    img_cropped = imutils.resize(img_cropped, width=500)

    # Draw the contours on the original image
    largestCountour = largestCountour.astype("float")
    largestCountour *= ratio
    largestCountour = largestCountour.astype("int")
    cv2.drawContours(img, [largestCountour], -1, (0, 255, 0), 2)

    return img_cropped

def detectLandmarks():
    global fld
    global rld

    # Reset all the number of landmarks before each verification
    Landmark.reset()

    # Detect landmarks for front side of MyKad
    fld = FrontLandmarkDetector(front_img_cropped.copy())
    fld.setCoordinates()
    fld.generateLandmarks()
    fld.drawLandmarks()
    fld.displayData()
    
    # Detect landmarks for rear side of MyKad
    rld = RearLandmarkDetector(rear_img_cropped.copy())
    rld.setCoordinates()
    rld.generateLandmarks()
    rld.displayData()

def detectFraudsAndSecurityFeatures():
    global fd
    
    # Detect frauds for both sides of MyKad
    fd = FraudDetector(front_img_cropped, rear_img_cropped)
    # Check images' blurriness
    fd.checkBlurriness(front_img_ratio, rear_img_ratio)

    # Decide whether to display the comparison results
    isDisplay = False

    totalFrontLandmarks = []
    totalRearLandmarks = []

    # FIXME
    # TODO: For better recognition?
    microprint = imutils.resize(fld.getLandmarks().microprint, width=500)
    twinTowers = imutils.resize(rld.getLandmarks().twinTowers, width=500)
    crown = imutils.resize(rld.getLandmarks().crown, width=500)
    malaysiaWord = imutils.resize(rld.getLandmarks().malaysiaWord, width=500)

    # Compare the landmarks on front side of MyKad
    totalFrontLandmarks.append(fd.compareLandmark('icLogoMatched', fld.getLandmarks().icLogo, cv2.imread('landmarks/lm_ic2.png',0), isDisplay))
    totalFrontLandmarks.append(fd.compareLandmark('mykadLogoMatched', fld.getLandmarks().myKadLogo, cv2.imread('landmarks/lm_mykad.png',0), isDisplay))
    totalFrontLandmarks.append(fd.compareLandmark('flagMatched', fld.getLandmarks().malaysiaFlag, cv2.imread('landmarks/lm_my-flag.png',0), isDisplay))
    totalFrontLandmarks.append(fd.compareLandmark('mscLogoMatched', fld.getLandmarks().mscLogo, cv2.imread('landmarks/lm_msc.png',0), isDisplay))
    totalFrontLandmarks.append(True) # IC Number
    totalFrontLandmarks.append(fd.compareLandmark('securityChipMatched', fld.getLandmarks().securityChip, cv2.imread('landmarks/lm_chip.png',0), isDisplay))
    totalFrontLandmarks.append(True) # Name
    totalFrontLandmarks.append(True) # Address
    totalFrontLandmarks.append(True) # Citizen
    totalFrontLandmarks.append(fd.compareLandmark('hibiscusMatched', fld.getLandmarks().hibiscus, cv2.imread('landmarks/lm_hibiscus.png',0), isDisplay))
    totalFrontLandmarks.append(fd.compareLandmark('microprintMatched', microprint, cv2.imread('landmarks/lm_microprint.png',0), isDisplay))

    # Compare the landmarks on rear side of MyKad
    totalRearLandmarks.append(fd.compareLandmark('coatOfArmsMatched', rld.getLandmarks().coatOfArms, cv2.imread('landmarks/lm_coa.png',0), isDisplay))
    totalRearLandmarks.append(fd.compareLandmark('tngMatched', rld.getLandmarks().touchNGo, cv2.imread('landmarks/lm_tng.png',0), isDisplay))
    totalRearLandmarks.append(fd.compareLandmark('atmMatched', rld.getLandmarks().atm, cv2.imread('landmarks/lm_atm.png',0), isDisplay))
    totalRearLandmarks.append(fd.compareLandmark('singatureMatched', rld.getLandmarks().headDirSign, cv2.imread('landmarks/lm_signature.png',0), isDisplay))
    totalRearLandmarks.append(True) # IC Number
    totalRearLandmarks.append(fd.compareLandmark('chipMatched', rld.getLandmarks().chip, cv2.imread('landmarks/lm_64k-chip.png',0), isDisplay))
    totalRearLandmarks.append(fd.compareLandmark('towersMatched', twinTowers, cv2.imread('landmarks/lm_towers.png',0), isDisplay))
    totalRearLandmarks.append(fd.compareLandmark('crownMatched', crown, cv2.imread('landmarks/lm_crown.png',0), isDisplay))
    totalRearLandmarks.append(fd.compareLandmark('malaysiaWordingMatched', malaysiaWord, cv2.imread('landmarks/lm_my.png',0), isDisplay))

    # Finalize all the actual landmarks only that are existed
    finalizeLandmarks(totalFrontLandmarks, totalRearLandmarks)

    fd.calculateValidLandmarks()

    # DATA CONSISTENCY VALIDATION
    # Verify whether there exists a valid NRIC
    fd.appendToString("isValidFrontNRIC", not np.array_equal(fld.getIcNum(),-1))
    fd.appendToString("isValidRearNRIC", not np.array_equal(rld.getIcNum(),-1))
    # Verify whether there exists a face, and append the result
    fd.appendToString("hasFace", not np.array_equal(fld.getFaces(),()))

    # Verify front and rear sides to see whether they are a pair, and append to result
    if(fld.getIcNum() == -1 or rld.getIcNum() == -1):
        fd.appendToString("isMyKadPair", False)
    else:
        fd.appendToString("isMyKadPair", np.array_equal(fld.getIcNum(),rld.getIcNum()))
    
def finalizeLandmarks(bool1, bool2):
    fld.drawActualLandmarks(bool1)
    rld.drawActualLandmarks(bool2)
    fld.appendLandmarkString()
    rld.appendLandmarkString()

    fld.appendToString("landmarkTotalNum", Landmark.getTotalNumCategoryOCR() + Landmark.getTotalNumCategoryPattern())
    fld.appendToString("landmarkFrontOCRNum", Landmark.getNumFrontCategoryOCR())
    fld.appendToString("landmarkFrontPatternNum", Landmark.getNumFrontCategoryPattern())
    fld.appendToString("landmarkRearOCRNum", Landmark.getNumRearCategoryOCR())
    fld.appendToString("landmarkRearPatternNum", Landmark.getNumRearCategoryPattern())
    fld.appendToString("landmarkTotalOCRNum", Landmark.getTotalNumCategoryOCR())
    fld.appendToString("landmarkTotalPatternNum", Landmark.getTotalNumCategoryPattern())

def getVerificationData():
    front_img_data = json.loads(str(fld))
    rear_img_data = json.loads(str(rld))
    fraud_img_data = json.loads(str(fd))

    allData = {**front_img_data, **rear_img_data, **fraud_img_data}

    result_data = finalizeVerification(allData)
    allData = {**allData, **result_data}

    return json.dumps(allData, indent=4)

def finalizeVerification(val):
    data = {}
    threshSecurityFeaturesScore = 50
    threshFraudsScore = 50
    threshFinalScore = 70

    # If either one of them is not satisfied, it is considered to fail the landmark detection
    if(not val['icLogoExistence'] or not val['mykadLogoExistence'] or not val['flagExistence'] or not val['securityChipExistence'] or not val['coatOfArmsExistence']):
        data.update({'landmarkDetectionPassed': False})
    else:
        data.update({'landmarkDetectionPassed': True})

    # If either one of them is not satisfied, it is considered to fail the security feature detection
    if(not val['microprintExistence'] or not val['microprintMatched']):
        data.update({'securityFeatureDetectionPassed': False})
    else:
        data.update({'securityFeatureDetectionPassed': True})

    # If either one of them is not satisfied, it is considered to fail the fraud detection
    if(not val['hasFace'] or not val['isMyKadPair']):
        data.update({'fraudDetectionPassed': False})
    else:
        data.update({'fraudDetectionPassed': True})

    # Continue to further computing the scores from landmark scores
    (l_currentScore, l_totalScore) = val['allLandmarksScore'].split('/')

    # Compute for security feature scores
    sf_currentScore = 0
    sf_totalScore = 0
    if(val['microprintExistence']):
        sf_currentScore += 1
    if(val['microprintMatched']):
        sf_currentScore += 1
    sf_totalScore += 2
    data.update({'thresholdSecurityFeaturesScore': threshSecurityFeaturesScore})
    data.update({'allSecurityFeaturesScore': "{}/{}".format(sf_currentScore, sf_totalScore)})
    data.update({'allSecurityFeaturesPercent': "{:.2f}".format(sf_currentScore / sf_totalScore * 100)})
    data.update({"securityFeaturesScorePassed": (sf_currentScore / sf_totalScore * 100) > threshSecurityFeaturesScore})

    # Compute for fraud scores
    f_currentScore = 0
    f_totalScore = 0
    if(val['hasFace']):
        f_currentScore += 1
    if(val['isMyKadPair']):
        f_currentScore += 1
    if(val['isValidFrontNRIC']):
        f_currentScore += 1
    if(val['isValidRearNRIC']):
        f_currentScore += 1
    if(val['name'] != ""):
        f_currentScore += 1
    if(val['address'] != ""):
        f_currentScore += 1
    if(not val['isFrontImageBlurred']):
        f_currentScore += 1
    if(not val['isRearImageBlurred']):
        f_currentScore += 1
    f_totalScore += 8
    data.update({'thresholdFraudsScore': threshFraudsScore})
    data.update({'allFraudsScore': "{}/{}".format(f_currentScore, f_totalScore)})
    data.update({'allFraudsPercent': "{:.2f}".format(f_currentScore / f_totalScore * 100)})
    data.update({"fraudsScorePassed": (f_currentScore / f_totalScore * 100) >= threshFraudsScore})

    # Compute for final verification scores
    currentScore = int(l_currentScore) + sf_currentScore + f_currentScore
    totalScore = int(l_totalScore) + sf_totalScore + f_totalScore
    data.update({'thresholdFinalScore': threshFinalScore})
    data.update({'finalScore': "{}/{}".format(currentScore, totalScore)})
    data.update({'finalPercent': "{:.2f}".format(currentScore / totalScore * 100)})
    data.update({"finalScorePassed": (currentScore / totalScore * 100) >= threshFinalScore})

    return data

def saveFinalImages():
    dirName = os.path.dirname(os.path.realpath(__file__))
    cv2.imwrite((dirName + r'\static\final-mykad-output\front.jpg'), fld.getMyKad(), [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    cv2.imwrite((dirName + r'\static\final-mykad-output\rear.jpg'), rld.getMyKad(), [int(cv2.IMWRITE_JPEG_QUALITY), 100])

@app.errorhandler(404) 
def default_handler(e):
    return render_template('error.html', errorCode='404')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/verification")
def verification():
    return render_template("verification.html")

@app.route("/statistics")
def statistics():
    data = pd.read_csv('./json-data/all-json.csv')
    return render_template("statistics.html", data=data)

@app.route("/about")
def about():
    return render_template("about.html")
	
@app.route("/result", methods=['GET', 'POST'])
def result():
    global front_img_cropped
    global rear_img_cropped

    if request.method == 'POST':
        img1 = request.form['front']
        img2 = request.form['rear']

        init(cv2.imread(img1),cv2.imread(img2))
        front_img_cropped = preprocessImage(front_img, front_img_thresh, front_img_ratio, front_img_resized)
        rear_img_cropped = preprocessImage(rear_img, rear_img_thresh, rear_img_ratio, rear_img_resized)

        detectLandmarks()
        detectFraudsAndSecurityFeatures()

        saveFinalImages()
        data = getVerificationData()
        return render_template('result.html', title="page", data=data)
    
    # If directly access /result without submitting the images
    return render_template('error.html', errorCode='400')

if __name__ == "__main__":
    app.run(debug=True)