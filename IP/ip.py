import cv2
import argparse as ap
import numpy as np

def detectSquare(cnt):
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.04*peri, True)
    if len(approx)== 4:
        return True
    return False
            
def newFilter(cnts):
    sqCnts = np.array([])
    for i in range (len(cnts)):
        cnt = cnts[i]
        if detectSquare(cnt):
            np.append(sqCnts, cnt, axis=0)
    return sqCnts
            
def filterForSquares(cnts):
    sqCnts = []
    for i in range (len(cnts)):
        cnt = cnts[i]
        if detectSquare(cnt):
            sqCnts.append(cnt)
    print("Square conts")
    print(len(sqCnts))
    print(len(cnts))
    outsider = []
    for i in range (len(cnts)):
        exist = False
        for j in range (len(sqCnts)):
            if np.array_equal(cnts[i], sqCnts[j]):
                exist = True
                break
        if not exist:
            outsider.append(cnts[i])
    #return outsider
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

    #perform some cleaning up via morphological operations.
    #--simple 3x3 kernel
    kernel = np.ones((3,3), np.uint8)
    eroded = cv2.erode(cannyImg, kernel, iterations = 1)
    dilate = cv2.dilate(cannyImg, kernel, iterations = 1)
    cv2.imshow("Dilated canny", dilate)
    
    #get contours.
    cannyContours = extractContours(cannyImg)
    directContours = extractContours(bottomHalf)
    dilatedContours = extractContours(dilate)
    
    filteredCnts, remainderCnts  = filterForSquares(dilatedContours)
    #testFilter = newFilter(dilatedContours)
    #testDF = cv2.dilate(testDF, kernel)
    #cv2.imshow("Test df", testDF)
    
    #draw contours.
    #--make a blank image.
    blackCanvas = createBlankImg(bottomHalf.shape[0], bottomHalf.shape[1])
    contouredImg = cv2.drawContours(blackCanvas, directContours, -1, (255,255,255), 1)
    dilatedCntImg = cv2.drawContours(blackCanvas, dilatedContours, -1, (255,255,255), 1)
    filteredBlackCanv = createBlankImg(bottomHalf.shape[0], bottomHalf.shape[1])
    rmdBlackCanv = createBlankImg(bottomHalf.shape[0], bottomHalf.shape[1])    
    filteredCntImg = cv2.drawContours(filteredBlackCanv, filteredCnts, -1, (255,255,255), 1)
    rmdCntImg =  cv2.drawContours(rmdBlackCanv, remainderCnts, -1, (255,255,255), 1)
    #largeSqCanv = createBlankImg(bottomHalf.shape[0], bottomHalf.shape[1])
    #largestSqCntImg = cv2.drawContours(largeSqCanv, largestSqCnt, -1, (255, 255, 255), 1)
    #cv2.imshow("Largest square contour", largestSqCntImg)
    cv2.imshow("Dilated contour", dilatedCntImg)
    cv2.imshow("Filtered squares contour", filteredCntImg)
    cv2.imshow("Remd cnt", rmdCntImg)

    #dilate filtereed contour image.
    dilatedFC  = cv2.dilate(filteredCntImg, kernel)
    cv2.imshow("DIlated fc", dilatedFC)
    cannyDilatedFC  = getCanny(dilatedFC)#canny to convert to binary
    dilatedExtractCnt = extractContours(cannyDilatedFC)
    cv2.imshow("cannydilated fc", cannyDilatedFC)
    filterDEC, rmd = filterForSquares(dilatedExtractCnt)
    print("FIlter num: " + str(len(filterDEC)) + " canny num: " + str(len(dilatedExtractCnt)))    
    preFilteredcCanv = createBlankImg(bottomHalf.shape[0], bottomHalf.shape[1])
    preFilcImg = cv2.drawContours(preFilteredcCanv, filterDEC, -1, (255,255,255), 1)
    cv2.imshow("Prefilteredc Img", preFilcImg)
    c = max(filterDEC, key=cv2.contourArea)
    cCanvas = createBlankImg(bottomHalf.shape[0], bottomHalf.shape[1])    
    singleCImg = cv2.drawContours(cCanvas, [c], 0, (255,255,255), 2)

    #get bounding rect.
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(singleCImg, (x,y), (x+w, y+h),(0,255,0), 2)

    #draw bounding rect on original bottom half
    tapedOnBottomHalf = cropBottomHalf(carPlateImg)    
    cv2.rectangle(tapedOnBottomHalf, (x,y), (x+w, y+h),(0,255,0), 2)    
    cv2.imshow("Single square img", singleCImg)
    cv2.imshow("Taped on bottom half", tapedOnBottomHalf)

    #crop region
    desiredRegion = cropRegion(tapedOnBottomHalf, y, x, y+h, x+w)
    print("desired region")
    print(desiredRegion)
    cv2.imshow("Cropped region", desiredRegion)



    #bitwise and
    extractedImg = cv2.bitwise_and(cannyImg, bottomHalf)
    cv2.imshow("Extracted Image", extractedImg)
    
    #cv2.imshow("Gray", gray)
    #cv2.imshow("Binarsied", binarised)
    cv2.imshow("Bottom half", bottomHalf)
    cv2.imshow("Canny", cannyImg)
    cv2.imshow("Contoured Image", contouredImg)
    cv2.imshow("Canny Erosion", eroded)
    cv2.waitKey(0)

