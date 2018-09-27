'''
use cv2.imshow(<filename>, imgVariable) to see the image.
make sure to include cv2.waitKey(0) at the end of the program.

For actual usage, dont use cv2.imshow along with cv2.waitKey(0) because it jams the program.
Instead, to use the images, just use cv2.imwrite(<filepath>, imgVar).

'''
import cv2
import argparse as ap
import numpy as np

def detectSquare(cnt):
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.04*peri, True)
    if len(approx)== 4:
        return True
    return False


def filterForSquares(cnts):
    sqCnts = []
    for i in range (len(cnts)):
        cnt = cnts[i]
        if detectSquare(cnt):
            sqCnts.append(cnt)
    #code below is relatively useless - was used for debug purposes.
    outsider = []
    for i in range (len(cnts)):
        exist = False
        for j in range (len(sqCnts)):
            if np.array_equal(cnts[i], sqCnts[j]):
                exist = True
                break
        if not exist:
            outsider.append(cnts[i])

    return [sqCnts, outsider]

def cropBottomHalf(img):
    half = int(img.shape[0]//2)
    cropped = img[half:]
    return cropped

def extractContours(img):
    im2, cnts, hier = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return cnts

def getCanny(img):
    edges = cv2.Canny(img, 50, 200)
    return edges

def createBlankImg(width, height, rgb_color=(0,0,0)):
    image = np.zeros((width, height, 3), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color
    return image

def cropRegion(img, p1, p2, p3, p4):
    region = []
    rowRegion = img[p1:p3]
    for i in range (len(rowRegion)):
        currRow = rowRegion[i]
        region.append(currRow[p2:p4])
    #region = rowRegion[p2:p4]

    return np.array(region, np.uint8)
if __name__ == "__main__":
    carPlateImg = cv2.imread("carPlateImg.jpg")
    gray = cv2.cvtColor(carPlateImg, cv2.COLOR_BGR2GRAY)

    #binarisation.
    ret, binarised = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    #get bottom half of the image.
    bottomHalf = cropBottomHalf(binarised)
    #find canny.
    cannyImg = getCanny(bottomHalf)

    #Dilate to get thicker lines -- might be pointless for now lmao.
    #--simple 3x3 kernel
    kernel = np.ones((3,3), np.uint8)
    dilate = cv2.dilate(cannyImg, kernel, iterations = 1)


    #get contours.
    dilatedContours = extractContours(dilate)

    #remainder cnts was used for debug purposes.
    filteredCnts, remainderCnts  = filterForSquares(dilatedContours)

    #draw contours.
    #--make a blank image.
    filteredBlackCanv = createBlankImg(bottomHalf.shape[0], bottomHalf.shape[1])
    filteredCntImg = cv2.drawContours(filteredBlackCanv, filteredCnts, -1, (255,255,255), 1)

    #dilate filtered contour image.
    dilatedFC  = cv2.dilate(filteredCntImg, kernel)

    cannyDilatedFC  = getCanny(dilatedFC)#canny to convert to binary
    dilatedExtractCnt = extractContours(cannyDilatedFC)


    #rmd was used for debug purposes.
    filterDEC, rmd = filterForSquares(dilatedExtractCnt)
    c = max(filterDEC, key=cv2.contourArea)

    #get bounding rect.
    x,y,w,h = cv2.boundingRect(c)
    #draw bounding rect on original bottom half
    tapedOnBottomHalf = cropBottomHalf(carPlateImg)
    #crop region
    desiredRegion = cropRegion(tapedOnBottomHalf, y, x, y+h, x+w)

    cv2.imwrite("carNumberPlate.jpg", desiredRegion)



