import cv2
import numpy as np
import json
from matplotlib import pyplot as plt

edgesSelected = 0
edgesCoordinates = []
minValues = None
maxValues = None
croppedCoordinates = []

imgPoints = np.array([[0,0], #GL
                         [519,4], #GD
                         [524,348], #DD
                         [3,347]], dtype=np.float32) #DL

objPoints = np.array([ (0.0 , 0.0, 0.0), #GL
                          (380.0 , 0.0 , 0.0), #GD
                          (380.0 , 250.0 , 0.0), #DD
                          (0.0 , 250.0 , 0.0)], dtype=np.float32) #DL

def selectEdge(event, x, y, flags, userData):
    
    global edgesSelected
    global edgesCoordinates
    global croppedCoordinates
    global minValues
    global maxValues
    
    if event == cv2.EVENT_LBUTTONDOWN:
        edgesCoordinates.append((x, y))
        if len(edgesCoordinates) >= 4:
            maxValues = np.array(edgesCoordinates[0])
            minValues = np.array(edgesCoordinates[0])
            for i in edgesCoordinates:
                if i[0] > maxValues[0]:
                    maxValues[0] = i[0]
                if i[1] > maxValues[1]:
                    maxValues[1] = i[1]
                if i[0] < minValues[0]:
                    minValues[0] = i[0]
                if i[1] < minValues[1]:
                    minValues[1] = i[1]
            edgesCoordinates = []
            cv2.destroyAllWindows()
            
def cutImage(ImageForCutting):
    return ImageForCutting[minValues[1]:maxValues[1],minValues[0]:maxValues[0]] 

def getRTheta(lines):
    for r,theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*r
        y0 = b*r  
        # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
        x1 = int(x0 + 1000*(-b))
        # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
        y1 = int(y0 + 1000*(a))
        # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
        x2 = int(x0 - 1000*(-b)) 
        # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
        y2 = int(y0 - 1000*(a))
        cv2.line(croppedImg,(x1,y1), (x2,y2), (0,0,255),2)   
    return r,theta

newParameters = input("Ukoliko zelite rekalibrirati kameru unesite 1, ukoliko zelite vec postojece psotavke unesite 2:")
if newParameters == "1":
    exec(open('calibration.py').read())
elif newParameters == "2":
    selectedImage = input("Unesite redni broj slike (1-3): ")     
    paperImage = cv2.imread("linijaMMpapir"+str(selectedImage)+".jpg")  #Stalna je slika budući se kamera crasha sa pokusajem uzivog prepoznavanja
    jsonFile = open("camera_params.json")
    jsonData = json.load(jsonFile)
    jsonFile.close()
    cameraMatrix = jsonData['camera_matrix']
    distCoeffs = jsonData['dist_coeffs']
    cameraMatrix = np.array(cameraMatrix)
    distCoeffs = np.array(distCoeffs)
    windName = "Unidstorted Image"
    undistortedImg = cv2.undistort(paperImage,cameraMatrix,distCoeffs)
    cv2.imshow(windName,undistortedImg)
    
    plt.figure(1)
    plt.imshow(undistortedImg)
    
    cv2.namedWindow(windName)
    cv2.setMouseCallback(windName,selectEdge)
    cv2.waitKey()

    undistImgCopy = undistortedImg.copy()
    croppedImg = cutImage(undistImgCopy)
    grayImage = cv2.cvtColor(croppedImg,cv2.COLOR_BGR2GRAY)
    edges= cv2.Canny(grayImage, 100, 140,apertureSize=3)
    lines = cv2.HoughLines(edges,1,np.pi/180, 70)
    plt.figure(3)
    plt.imshow(croppedImg)
    Ro, theta = getRTheta(lines)
    plt.figure()
    plt.imshow(croppedImg) 
    plt.xlabel("Kut izmedu pravca i x osi je: " + str(theta*57.2957795))
    cv2.imwrite('linesDetected.jpg', croppedImg)
    
    ret,rvec,tvec = cv2.solvePnP(objPoints,imgPoints,cameraMatrix,distCoeffs)
    rotationMat, JB = cv2.Rodrigues(rvec)
    A=cameraMatrix @ rotationMat
    B=cameraMatrix @ tvec
    
    lx = A[0, 0] * np.cos(theta) + A[1, 0] * np.sin(theta) - Ro * A[2, 0]
    ly = A[0, 1] * np.cos(theta) + A[1, 1] * np.sin(theta) - Ro * A[2, 1]
    lr = B[2] * Ro - B[0] * np.cos(theta) - B[1] * np.sin(theta)
    realTheta = np.arctan2(ly, lx)
    realRho = lr / np.sqrt(lx**2 + ly**2)
    
    print("Prava theta: " + str(realTheta))
    print("Pravi rho: " + str(realRho))

    
    


