import cv2 as cv
import numpy as np
import json
import random
from matplotlib import pyplot as plt
import convert_2d_points_to_3d_points
import plot_3d_points

cameraParamsMatrix = [[346.40640259, 0.0, 180.93818665], 
                      [0.0, 341.74661255, 101.59582520], 
                      [0.0, 0.0,  1.0]]


imageL= cv.imread("imageL.bmp")
imageR= cv.imread("imageR.bmp")
#----------------------------------------------------------
imageL_grayscale = cv.cvtColor(imageL, cv.COLOR_BGR2GRAY)
imageR_grayscale = cv.cvtColor(imageR, cv.COLOR_BGR2GRAY)
#----------------------------------------------------------
sift=cv.xfeatures2d.SIFT_create()
keypointsL, desL = sift.detectAndCompute(imageL_grayscale, None)
keypointsR, desR = sift.detectAndCompute(imageR_grayscale, None)
#----------------------------------------------------------
imageL_sift = cv.drawKeypoints(imageL,keypointsL,None)
plt.figure(1)
plt.imshow(imageL_sift)
imageR_sift = cv.drawKeypoints(imageR,keypointsR,None)
plt.figure(2)
plt.imshow(imageR_sift)
#----------------------------------------------------------

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

#flann = cv.FlannBasedMatcher(index_params, search_params)
flann =  cv.DescriptorMatcher_create(1)
parovi = flann.knnMatch(desL,desR,k=2)

#bf=cv.BFMatcher()
#parovi= bf.knnMatch(desL,desR,k=2)
#----------------------------------------------------------
#Filtriranje parova
dobri_parovi = []
newLeftPoints = []
newRightPoints = []
for m,n in parovi:
    if m.distance < 0.75*n.distance:
        dobri_parovi.append([m])
        newLeftPoints.append(keypointsL[m.queryIdx].pt)
        newRightPoints.append(keypointsR[m.trainIdx].pt)
matched_image= cv.drawMatchesKnn(imageL,keypointsL,imageR,keypointsR,dobri_parovi,
                                 None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
plt.figure(3)
plt.imshow(matched_image)
plt.title("Filtering Matches")
#----------------------------------------------------------
#FundamentalMatrixTime
ptsLAsArray = np.asarray(newLeftPoints)
ptsRAsArray = np.asarray(newRightPoints)
   
leftFilteredKeypoints = []
rightFilteredKeypoints= []
#----------------------------------------------------------
FundamentalMatrix, mask = cv.findFundamentalMat(ptsLAsArray, ptsRAsArray, cv.FM_RANSAC)
im_h = cv.hconcat([imageL, imageR])


for i in range (0,mask.shape[0]):
    random_color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    if (mask[i] == 1):
        leftFilteredKeypoints.append(cv.KeyPoint(ptsLAsArray[i,0],ptsLAsArray[i,1],1))
        im_h = cv.circle(im_h,(int(ptsLAsArray[i,0]),int(ptsLAsArray[i,1])) , 2, random_color, 2)
        rightFilteredKeypoints.append(cv.KeyPoint(ptsRAsArray[i,0],ptsRAsArray[i,1],1))
        im_h = cv.circle(im_h,(int(ptsRAsArray[i,0])+320,int(ptsRAsArray[i,1])) , 2, random_color, 2)
        cv.line(im_h, (int(ptsLAsArray[i,0]),int(ptsLAsArray[i,1])), (int(ptsRAsArray[i,0])+320,int(ptsRAsArray[i,1])), random_color,2)
plt.figure(5)
plt.imshow(im_h)       
plt.title("SoloQ printed good matches")
cameraParamsTransposedwithFundamentalMatrix= np.matmul(FundamentalMatrix,np.transpose(cameraParamsMatrix))
EssentialMatrix= np.matmul(cameraParamsTransposedwithFundamentalMatrix,cameraParamsMatrix)
#----------------------------------------------------------
#CREATING 3D POINTS
EssentialMatrix = np.matrix(EssentialMatrix)
cameraParamsMatrix = np.matrix(cameraParamsMatrix)
        
new3DPoints = convert_2d_points_to_3d_points.convert_2d_points_to_3d_points(leftFilteredKeypoints, 
                                                                            rightFilteredKeypoints, EssentialMatrix, cameraParamsMatrix)

outputFile = open('points_3d.json',"w")
if(outputFile is None):
        print("\nProblem with writing to the file..")
        quit()
json.dump(new3DPoints.tolist(),outputFile)
print("\n3D Tocke su zapisane u JSON datoteku.")
#plot_3d_points.main()