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
    cap = cv2.VideoCapture("basementFootage.mp4")
    
    ret, prevFrame = cap.read()
    prevGFrame = cv2.cvtColor(prevFrame, cv2.COLOR_BGR2GRAY)
    prevGFrame = cv2.GaussianBlur(prevGFrame, (21, 21), 0)
    ret2, prevGFrame = cv2.threshold(prevGFrame, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    first = True
    startTime = time.time()
    counter = 0
    timeGraph = []
    diffPixGraph = []
    while True:
        ret, currFrame = cap.read()
        if ret:
            currGFrame = cv2.cvtColor(currFrame, cv2.COLOR_BGR2GRAY)
            currGFrame = cv2.GaussianBlur(currGFrame, (21, 21), 0)
            ret2, currGFrame = cv2.threshold(currGFrame, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            
            #cv2.imshow("vid", currGFrame)            
            #cv2.imshow("Color", currFrame)
            #subtract frames
            #if counter % 10 == 0:
            if first:
                first = False
                prevSubtracted = cv2.bitwise_and(currGFrame, cv2.bitwise_not(prevGFrame))
            else:
                subtracted = cv2.bitwise_and(currGFrame, cv2.bitwise_not(prevGFrame))
                currDiffPixNum = np.sum(subtracted == 255)
                prevDiffPixNum = np.sum(prevSubtracted == 255)
                changeInChange = currDiffPixNum - prevDiffPixNum
                currTime = time.time() - startTime
                #diffPixNum = np.sum(subtracted == 255)
                timeGraph.append(currTime)
                diffPixGraph.append(changeInChange)
                prevSubtracted = subtracted
                
                #if subtracted frame difference crosses a threshold, motion is detected.
                if False:
                    motionDetected = True
                cv2.imshow("Subtracted", subtracted)


                
            #After processing, set prevFrame to currFrame
            prevFrame = currFrame
            prevGFrame = currGFrame
            
            if motionDetected:
                timeCounter = 0
            if timeCounter >= timeout:
                motionDetected = False

            timeCounter += 1
            cv2.waitKey(20)
        else:
            break
        counter += 1

    plt.plot(timeGraph, diffPixGraph)
    plt.show()
    cap.release()
    cv2.destroyAllWindows()
     
