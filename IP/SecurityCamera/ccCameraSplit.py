'''
timeout is how long it takes for the lights in a motionless area to turn dim.
cv.imshow() and cv.waitKey() will probably cause the program to jam as it tries to load the video. So, if you're facing crashing issues, you can comment them out.
I left them in because I feel that they show crucial information on how it works.
'''
import os
import imutils
import cv2
import argparse as ap
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt

class MDEntity:
    def __init__(self, callback):
        self.cb = callback
        self.avgFrame = None
        self.firstGFrame = None
        self.timeCounter = 0
        self.timeout = 100
        self.motionDetected = False
        self.actualMotion = False
        self.flipped = False
        self.text = "No motion"

    def processImage(self, frame):
        currFrame = imutils.resize(frame, width=500)
        currGFrame = cv2.cvtColor(currFrame,cv2.COLOR_BGR2GRAY)
        #apply blurring to smooth the image. - Important preprocessing.
        currGFrame = cv2.GaussianBlur(currGFrame, (21,21), 0)

        #TODO: This code is questionable.. but I'm too lazy to look into it.
        if self.firstGFrame is None:
            self.firstGFrame = currGFrame
            self.avgFrame = currGFrame.copy().astype("float")
            return
        cv2.accumulateWeighted(currGFrame, self.avgFrame,0.2)
        frameDelta = cv2.absdiff(cv2.convertScaleAbs(self.avgFrame), currGFrame)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        if np.sum(thresh == 255) > 0:
            self.motionDetected = True
            #if detected motion, reset timer.
            self.timeCounter = 0
        else :
            self.motionDetected = False
            self.timeCounter += 1

        #actual motion switch flipping.
        if self.motionDetected:
            if not self.actualMotion:
                self.actualMotion = True
                self.flipped = True
        else:
            if self.timeCounter >= self.timeout and self.actualMotion:
                self.actualMotion = False
                self.flipped = True


        #if flipped, send to dim or send to brighten.
        if self.flipped:
            #callback to brighten lights here.
            if self.actualMotion:
                #send light signal to turn on.
                now = datetime.datetime.now()
                nowStr = str(now.hour) +":" + str(now.minute) + ":"+str(now.second) + " "+ str(now.day) + "/" + str(now.month) + "/" + str(now.year)
                self.cb(1, nowStr)
                self.text = "Motion detected"
            else:
                #we can set a callback to dim lights here as well.
                #for future reference.
                now = datetime.datetime.now()
                nowStr = str(now.hour) +":" + str(now.minute) + ":"+str(now.second) + " "+ str(now.day) + "/" + str(now.month) + "/" + str(now.year)
                self.text = "No motion"
                self.cb(0, nowStr)


        #cv2.putText(currFrame, "Obs: {}".format(self.text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        self.flipped = False

        return self.text;


