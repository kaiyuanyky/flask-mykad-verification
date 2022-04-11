# Flask MyKad Verification
A web service to verify the MyKad document by using the multi-factor algorithm that is developed using Python. 
The web service is developed using Flask, and it is demonstrated on the web application.

## Overview
- Verify the MyKad documents of the users by using a web application, with the image of MyKad sent from the web page to the web service for processing.
- In this process, the images are separated into key features that are used to identify and verify the users based on specific criteria.
- These key features include the detections from aspects of landmarks, security features, and fraud.

## Goals
- To design the algorithms for the web service of verifying a MyKad document with different aspects of detections.
- To improve the accuracy of verification using this multi-factor verification.

## How to Install/Run
1. Download the source code.
2. Open the source code folder in **Visual Studio Code**.
3. Install **Tesseract OCR** engine.
4. Modify the OCR path in `FrontLandmarkDetector.py` and `RearLandmarkDetector.py`.
5. Install the packages using the following:

```python
pip install -r requirements.txt
```

## How to Run
1. Enter the following command in your current working directory:

```python
py main.py
```

2. Access the web service locally on your browser with the URL [http://127.0.0.1:5000](http://127.0.0.1:5000).
2. Alternatively, click [here](https://mykad.herokuapp.com/) for direct access.

## Technological Background
- OpenCV
- Python
- Flask
- Tesseract OCR
- HTML, CSS, JS
- Bootstrap
- jQuery
- Swiper.js
- Chart.js