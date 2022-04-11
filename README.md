# Flask MyKad Verification
A web service to verify the MyKad document by using the multi-factor algorithm that is developed using Python. 
The web service is developed using Flask, and it is demonstrated on the web application.

## Overview
- Verify the MyKad documents of the users by using a web application, with the image of MyKad sent from the web page to the web service for processing.
- In this process, the images are separated into key features that are used to identify and verify the users based on specific criteria.
- These key features include the detections from aspects of landmarks, security features, and fraud.

## Goals
1. To design the algorithms for the web service of verifying a MyKad document with different aspects of detections.
2. To improve the accuracy of verification using this multi-factor verification.

## How to Install
1. Download the source code and extract it to your working folder manually.
2. Alternatively, clone this repository into your working folder using the following command.

```
git clone https://github.com/kaiyuanyky/flask-mykad-verification.git
```

3. Open the source code folder in **Visual Studio Code**.
4. Install the required packages using the following command:

```python
pip install -r requirements.txt
```

## How to Run
1. In your current working folder, enter the following command:

```python
py main.py
```

## How to Use
1. Open the URL [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser to access the web service locally.
2. Alternatively, click [here](https://mykad.herokuapp.com/) to access the web service directly.

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