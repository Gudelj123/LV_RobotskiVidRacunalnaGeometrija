import cv2
import random
import numpy as np
#############################################################################
##              LV2 - Podjela ravnina na poligone
#Izraditi konzolnu aplikaciju koja:
#1. generira 20 nasumično izabranih točaka unutar kvadrata dimenzije 400 piksela;
#2. generira Delaunay triangulaciju skupa točaka iz koraka 1;
#3. prikazuje triangulaciju dobivenu u koraku 2 u prozoru dimenzija 440 x 440;
#4. omogućuje izbor nekog od trokuta triangulacije klikom lijeve tipke miša;
#5. izabrani trokut prikazuje crvenom bojom, a njemu susjedne trokute (one
#   koji s njim dijele zajedničku stranicu) prikazuje plavom bojom. 
#############################################################################
#           Funkcije koje služe za dohvaćanje rubova odnosno trokuta
#############################################################################
#Zadatak funkcije je dohvatiti sljedeći rub.
def getNextEdge(edge, subDivision):
    return subDivision.getEdge(edge, 0b00010011)

#Funkcija ispod ima zadatak primiti jedan rub kao argument te potom proći kroz ostale
#rubove i vratiti točke trokuta
def getTriangle(firstEdge, subDivision):
    edge1Origin = subDivision.edgeOrg(int(firstEdge))[1]
    edge1Destination = subDivision.edgeDst(int(firstEdge))[1]      
    secondEdge = getNextEdge(firstEdge, subDivision)
    edge2Origin = edge1Destination
    edge2Destination = subDivision.edgeDst(secondEdge)[1]     
    edge3Origin = edge2Destination
    triangle = np.array([[edge1Origin[0], edge1Origin[1]],[edge2Origin[0], edge2Origin[1]],[edge3Origin[0], edge3Origin[1]]], dtype=np.int32)
    return triangle
#############################################################################
#############################################################################
#           On-Mouse Click Event koji se pokrene klikom na trokut
#############################################################################

def onClickEvent(event, x, y, flags, userData):
    if event == cv2.EVENT_LBUTTONDOWN:
        subDivision = userData[0]
        image = np.copy(userData[2]) 
        windowName = userData[1]      
        firstEdge = subDivision.locate((x, y))[1] 
        mainTriangle = getTriangle(firstEdge, subDivision)
        triangle1 = getTriangle(subDivision.rotateEdge(firstEdge, 2), subDivision)       
        secondEdge = getNextEdge(firstEdge, subDivision)
        triangle2 = getTriangle(subDivision.rotateEdge(secondEdge, 2), subDivision)       
        thirdEdge = getNextEdge(secondEdge, subDivision)
        triangle3 = getTriangle(subDivision.rotateEdge(thirdEdge, 2), subDivision)      
        cv2.fillConvexPoly(image, mainTriangle, (0, 0, 255))
        cv2.fillConvexPoly(image, triangle1, (255, 0, 0))
        cv2.fillConvexPoly(image, triangle2, (255, 0, 0))
        cv2.fillConvexPoly(image, triangle3, (255, 0, 0))
        cv2.imshow(windowName, image)
#############################################################################
#############################################################################
#              Funkcije za podjelu ravnine i dodavanje točaka u istu
############################################################################# 
  
#Funkcija čiji je zadatak kreiranje podjele slike na subdivizije
def createSubDivPlain(picSize):
    square = (0, 0, picSize, picSize) 
    return cv2.Subdiv2D(square)

#Dodavanje točki u unaprijed podjeljenu ravninu
def createRandomPointsInPlain(subDivision, pointNumber, side):
    for i in range(pointNumber): 
        point = (random.randint(1, side - 1), random.randint(1, side - 1))
        subDivision.insert(point)
        
#############################################################################        
#############################################################################
#               Funkcije za iscrtavanje Delaunay Triangulacije
#############################################################################

#Funkcija koja prima sve točke koji predstavljaju vrhove trokuta te se u njoj iscrtavaju
# trokutovi Delaunay triangulacije
def drawDelaunayTriangle(image, triangleVertices):
    lineColor = (0, 0, 0)
    lineThickness = 3
    intVertices = []
    for i in range(len(triangleVertices)):
        intVertices.append(int(triangleVertices[i]))
    point1 = (intVertices[0], intVertices[1])
    point2 = (intVertices[2], intVertices[3])
    point3 = (intVertices[4], intVertices[5])
    cv2.line(image, point1, point2, lineColor, lineThickness)
    cv2.line(image, point2, point3, lineColor, lineThickness)
    cv2.line(image, point3, point1, lineColor, lineThickness)

#Funkcija kojoj se predaje čista slika, podjela na subdivizije(područja),
# te ime prozora koja za zadatak ima prikazivanje Delaunay triangulacije
def showDelaunayTriangulation(image, subDivision, windowName):
    triangleList = subDivision.getTriangleList()
    for i in range(len(triangleList)):
        drawDelaunayTriangle(image, triangleList[i])
    cv2.imshow(windowName, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 
           
############################################################################# 
#############################################################################       
def main():
    windowSize = 440
    picSize = 400
    numberOfPoints = 20
    windowName = "Gudelj - Delaunay Triangulation"
    subDivision = createSubDivPlain(picSize)
    image = np.full((windowSize, windowSize, 3), 255, dtype=np.uint8)
    cv2.namedWindow(windowName)
    cv2.setMouseCallback(windowName, onClickEvent, [subDivision, windowName, image])
    createRandomPointsInPlain(subDivision, numberOfPoints, picSize)
    showDelaunayTriangulation(image, subDivision, windowName)
    
    
if __name__ == "__main__":
    main()