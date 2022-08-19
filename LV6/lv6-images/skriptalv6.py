import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
def my_first_initializer(coef_):
    global coef
    coef = coef_ 

#****************************************************
def read_kinect_pic(depth_path, image_shape):
    depth_map = np.zeros(image_shape)
    depth_image = np.zeros(image_shape[:2], dtype=np.uint8)

    point_3d_array = []

    d_min = 2047
    d_max = 0    

    with open(depth_path, 'r') as f:
        depth_data = f.read().strip().split('\n')
        depth_data = [row.strip().split(' ') for row in depth_data]
        for v, row in enumerate(depth_data):
            for u, d in enumerate(row):
                d = int(d)
                if d == 2047:
                    d = -1
                else:
                    if d < d_min:
                        d_min = d
                    if d > d_max:
                        d_max = d

                    point_3d_array.append([u, v, d])

                depth_map[v, u] = d

        for v, row in enumerate(depth_data):
            for u, d in enumerate(row):
                d = int(d)
                if d != -1:
                    d = (d - d_min) * 254 // (d_max - d_min) + 1
                    depth_image[v, u] = d

    n_3d_points = len(point_3d_array)

    return depth_image, point_3d_array, n_3d_points
#****************************************************
#****************************************************
#Primjenjivanje RANSAC algoritma iz priloga vježbe
def ransac(point3DArray):
    randomNumberGen = np.random.default_rng()
    Tstar = []
    Rstar = []
    
    for i in range(100):
        hasInverse = False # Varijabla za provjeru ima li newMatrix inverz
        while not hasInverse:
            newMatrix = []
            distanceVector = []
            #Unutar petlje odabiremo 3 točke slučajnim izborom i formiramo potrebne matrice i vektore 
            for j in range(0, 3):
                index = randomNumberGen.integers(0, len(point3DArray), 1)[0]
                point3D = point3DArray[index]
                temp = point3D[:-1]
                temp.append(1)
                newMatrix.append(temp)
                d = point3D[-1]
                distanceVector.append(d)
            newMatrix = np.matrix(newMatrix, dtype = np.float32)
            distanceVector = np.array(distanceVector, dtype = np.float32)
            distanceVector = distanceVector.reshape(-1, 1)
            hasInverse, R = cv.solve(newMatrix, distanceVector) #Rješavanje jednadžbe za pronalazak a, b i c nove matrice R
            
        T = []
        a = R[0, 0]
        b = R[1, 0]
        c = R[2, 0]
        for newPoint in point3DArray:
            p1 = newPoint[0]
            p2 = newPoint[1]
            p3 = newPoint[2]
            dif = abs(p3 - (a * p1 + b * p2 + c))
            if dif < 2:
                T.append(newPoint)
        
        #Ima li na ovoj ravnini vise tocaka od trenutne dominantne
        if len(T) > len(Tstar):
            Tstar = T
            Rstar = R
    
    return Tstar
#****************************************************
#****************************************************

numOfPic = int(input("Unesite broj slike (1-9): "))
 
if (numOfPic >= 1 and numOfPic <=9):
   imagePath = "sl-0000"+str(numOfPic)+ ".bmp"
   depthPath = "sl-0000"+str(numOfPic)+"-D.txt"
   realImage = cv.imread(imagePath)
   shapeOfImage = np.shape(realImage)
   depthImage, point3DArray, n3DPoints = read_kinect_pic(depthPath, shapeOfImage)
   plt.figure(1)
   plt.imshow(realImage)
   plt.title("OG image")   
   plt.figure(2)
   plt.imshow(depthImage)
   plt.title("Depth Image")

   dominantArguments = [point3DArray]
   dominantArguments = np.asarray(point3DArray, dtype= np.float64)
   DominantPlanePoints = tqdm(ransac(point3DArray))
   #Iscrtavanje točaka dominantne ravnine
   for tempPoint in DominantPlanePoints:
       pointsToDraw = (tempPoint[0],tempPoint[1])
       cv.circle(depthImage,pointsToDraw, radius=0, color=(0,255,0),thickness=-1)
   plt.figure(3)
   plt.imshow(depthImage)
   plt.title("Pronadena je dominantna ravnina")

