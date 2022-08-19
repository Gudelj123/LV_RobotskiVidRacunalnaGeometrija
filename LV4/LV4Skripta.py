#LV4 - Gudelj

import cv2 
import matplotlib.pyplot as plt
import numpy as np

# read images
img1 = cv2.imread('ImageT0.jpg')  
img2 = cv2.imread('ImageT2.jpg') 

img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

figure, ax = plt.subplots(1, 2, figsize=(16, 8))
ax[0].imshow(img1, cmap='gray')
ax[1].imshow(img2, cmap='gray')
  
# Select ROI
newWindowCoordinates = cv2.selectROI("select the area", img1)
  
# Crop image
cropped_image = img1[int(newWindowCoordinates[1]):int(newWindowCoordinates[1]+newWindowCoordinates[3]), 
                      int(newWindowCoordinates[0]):int(newWindowCoordinates[0]+newWindowCoordinates[2])]

sift = cv2.xfeatures2d.SIFT_create()
keypoints_1, descriptors_1 = sift.detectAndCompute(cropped_image,None)
keypoints_2, descriptors_2 = sift.detectAndCompute(img2,None)
plt.figure(1)
plt.imshow(cv2.drawKeypoints(cropped_image,keypoints_1,cropped_image))
plt.figure(2)
plt.imshow(cv2.drawKeypoints(img2,keypoints_2,img2))

bruteForcer = cv2.BFMatcher()
parovi = bruteForcer.knnMatch(descriptors_1,descriptors_2,k=2)

bruteForcerShow = cv2.BFMatcher()
parovizaShow = bruteForcerShow.match(descriptors_1,descriptors_2)
sorted_parovi = sorted(parovizaShow, key = lambda x:x.distance)
img3 = cv2.drawMatches(cropped_image, keypoints_1, img2, keypoints_2, sorted_parovi[:50], img2, flags=2)
plt.figure(3)
plt.imshow(img3),plt.show()


FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)
#bf = cv2.BFMatcher()
matches = flann.knnMatch(descriptors_1,descriptors_2,k=2)

good = []
for m,n in matches :
    if m.distance < 0.7*n.distance :
        good.append(m)

MIN_MATCH_COUNT = 3

if len(good)>MIN_MATCH_COUNT:
    src_pts = np.float32([ keypoints_1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ keypoints_2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    h,w = cropped_image.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)

    img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
    

else:
    matchesMask = None

draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)

img3 = cv2.drawMatches(cropped_image,keypoints_1,img2,keypoints_2,good,None,**draw_params)

plt.imshow(img3),plt.show()
cv2.imwrite('matches.jpg',img3)



