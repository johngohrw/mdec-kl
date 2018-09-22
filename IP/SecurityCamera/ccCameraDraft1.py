'''
use cv2.imshow(<filename>, imgVariable) to see the image.
make sure to include cv2.waitKey(0) at the end of the program.

For actual usage, dont use cv2.imshow along with cv2.waitKey(0) because it jams the program.
Instead, to use the images, just use cv2.imwrite(<filepath>, imgVar).

'''
import cv2
import argparse as ap
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt
if __name__ == "__main__":
    #set timeout timer.
    timeout = 100000 #arbitrary value.
    timeCounter = 0

    #motion detected flag.
    motionDetected = False
    #read video.
    cap = cv2.VideoCapture("motionTest.mp4")
    #cap = cv2.VideoCapture("basementFootage.mp4")
    
    ret, prevFrame = cap.read()
    prevGFrame = cv2.cvtColor(prevFrame, cv2.COLOR_BGR2GRAY)
    ret2, prevGFrame = cv2.threshold(prevGFrame, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    first = True
    startTime = time.time()
    counter = 0
    timeGraph = []
    diffPixGraph = []
    ret, firstFrame = cap.read()
    firstGFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
    firstGFrame = cv2.GaussianBlur(firstGFrame, (21, 21), 0)
    #firstGFrame = cv2.threshold(firstGFrame, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    while True:
        ret, currFrame = cap.read()
        if ret:
            currGFrame = cv2.cvtColor(currFrame,cv2.COLOR_BGR2GRAY)
            currGFrame = cv2.GaussianBlur(currGFrame, (21,21), 0)
            #ret2, currGFrame = cv2.threshold(currGFrame, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)            
            frameDelta = cv2.absdiff(firstGFrame, currGFrame)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
            cv2.imshow("Frame delta", thresh)
            cv2.imshow("Original", currFrame)
            cv2.waitKey(20)
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
     
