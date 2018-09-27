'''
use cv2.imshow(<filename>, imgVariable) to see the image.
make sure to include cv2.waitKey(0) at the end of the program.

For actual usage, dont use cv2.imshow along with cv2.waitKey(0) because it jams the program.
Instead, to use the images, just use cv2.imwrite(<filepath>, imgVar).

'''
import cv2
import argparse as ap
import numpy as np
def createBlankImg(width, height, rgb_color=(0,0,0)):
    image = np.zeros((width, height, 3), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color
    return image

def detectSquare(cnt):
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.04*peri, True)
    if len(approx)== 4:
        return True
    return False
            
def showResized(imgName, img, newSize=(720, 560)):
    tmp = img.copy()
    resized = cv2.resize(tmp, newSize)
    cv2.imshow(imgName, resized)

    
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
    carPlateImg = cv2.imread("carPlateImg2.png")
    gray = cv2.cvtColor(carPlateImg, cv2.COLOR_BGR2GRAY)

    showResized("Original", carPlateImg)
    showResized("Gray", gray)

    #--Notes: clahe is supposedly better at bringing more balance foregrounds
    #we dont really need this for now because the headlights of cars are too bright.
    #we would rather have an overexposed foreground as long as we can clearly see the number plate.
    #CLAHE histogram equalization.
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    claheImg = clahe.apply(gray)
    showResized("Clahe-d", claheImg)
    
    vis = carPlateImg.copy()
    #Create MSER
    mser = cv2.MSER_create()
    #--MSER algo.

    clVis = carPlateImg.copy()
    clRegions, _ = mser.detectRegions(claheImg)
    clHulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in clRegions]
    cv2.polylines(clVis, clHulls, 1, (0,255,0))
    showResized("Clahe MSER Region", clVis)
    #NOTE: from sample image, CLAHE seems to produce better results (with MSER) than standard Histogram equlization as mentioned in the paper. 

    gFiltered = cv2.GaussianBlur(gray, (21,21), 0)
    showResized("Blurred", gFiltered)

    #find canny.
    cannyImg = getCanny(gray)
    showResized("Canned", cannyImg)
    cv2.imwrite("mserRegion.jpg", clVis)
    cv2.imwrite("canned.jpg", cannyImg)

    #dilate mser regions.
    kernel = np.ones((3,3), np.uint8)
    dilate = cv2.dilate(clVis, kernel, iterations = 3)
    showResized("Dilated mser", dilate)
    cannyDilated = getCanny(dilate)
    im2, cnts, hier = cv2.findContours(cannyDilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    tapedOnImg = carPlateImg.copy()
    filteredCnts, remd = filterForSquares(cnts)
    filteredCntImg = createBlankImg(dilate.shape[0], dilate.shape[1])
    for i in range (len(filteredCnts)):
        x,y,w,h = cv2.boundingRect(filteredCnts[i])
        cv2.rectangle(tapedOnImg,(x,y), (x+w,y+h),(0,255,0),2)
    showResized("Bounding rects", tapedOnImg)
    
    cv2.waitKey(0)


    

