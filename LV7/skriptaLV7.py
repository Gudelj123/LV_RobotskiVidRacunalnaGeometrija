import vtk
import time
from vtkmodules.vtkCommonDataModel import vtkIterativeClosestPointTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkRenderingCore import vtkRenderer
from vtkmodules.vtkRenderingCore import vtkRenderWindow
from vtkmodules.vtkRenderingCore import vtkRenderWindowInteractor
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkRenderingCore import vtkPolyDataMapper
from vtkmodules.vtkRenderingCore import vtkActor
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkRenderingCore import vtkTextActor
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor 
from vtkmodules.vtkInteractionWidgets import vtkScalarBarWidget

NUMBER_OF_ITERATIONS=50
NUMBER_OF_LANDMARKS=50
lut = vtkLookupTable()
lut.Build()
  
#Učitavanje modela odlomka (Taj treba fitat)
###########################################
partialPlyReader = vtkPLYReader()
partialPlyReader.SetFileName('modeli/bunny_t4_parc.ply')
partialPlyReader.Update()
inputPartialPlyReader = partialPlyReader.GetOutput()
###########################################

#Učitavanje modela cijelog zeca
###########################################
fullPlyReader = vtkPLYReader()
fullPlyReader.SetFileName('modeli/bunny.ply')
fullPlyReader.Update()
targetedinputPlyReader = fullPlyReader.GetOutput()
###########################################

#Pokretanje timera za mjerenje vremena potrebnog za matchanje landmarka
startingTime = time.time()

icp = vtkIterativeClosestPointTransform()
#Podešavanje izvornog modela koji treba fit-at
icp.SetSource(inputPartialPlyReader) 
#Postavljanje ciljanog modela na koji fit-amo izvorni model
icp.SetTarget(targetedinputPlyReader) 
icp.GetLandmarkTransform().SetModeToRigidBody() 
#   Postavljanje postavki vezano za broj iteracija algoritma i 
#   obilježja po kojima se modeli matchaju
icp.SetMaximumNumberOfIterations(NUMBER_OF_ITERATIONS) 
icp.SetMaximumNumberOfLandmarks(NUMBER_OF_LANDMARKS) 
icp.Update() 

icpTransformFilter = vtkTransformPolyDataFilter()
icpTransformFilter.SetInputData(inputPartialPlyReader) 
icpTransformFilter.SetTransform(icp) 
icpTransformFilter.Update()
icpResult = icpTransformFilter.GetOutput()

#Zaustavljanje timera za mjerenje vremena potrebnog za matchanje landmarka
endingTime = time.time()
timeDifference = endingTime - startingTime



#CRVENI ZEC - POČETNA POZICIJA ODLOMKA
###########################################
polyDataMapper = vtkPolyDataMapper()
polyDataMapper.SetInputData(inputPartialPlyReader)

primaryActor = vtkActor()
primaryActor.SetMapper(polyDataMapper) 
primaryActor.GetProperty().SetColor(1.0, 0.0, 0.0) 
primaryActor.GetProperty().SetPointSize(5) 
###########################################

#ZELENI ZEC - CILJANA POZICIJA NA CIJELOM ZECU
###########################################
secondaryPolyaDataMapper = vtkPolyDataMapper()
secondaryPolyaDataMapper.SetInputData(targetedinputPlyReader)

secondaryActor = vtkActor()
secondaryActor.SetMapper(secondaryPolyaDataMapper) 
secondaryActor.GetProperty().SetColor(0.0, 1.0, 0.0) 
secondaryActor.GetProperty().SetPointSize(5) 
###########################################

#PLAVI ZEC - REZULTAT TRANZICIJE
###########################################
theraryPolyDataMapper = vtkPolyDataMapper()
theraryPolyDataMapper.SetInputData(icpResult)

theraryActor = vtkActor()
theraryActor.SetMapper(theraryPolyDataMapper) 
theraryActor.GetProperty().SetColor(0.0, 0.0, 1.0) 
theraryActor.GetProperty().SetPointSize(5)
########################################### 


#Pokušaj textActora
###########################################
textActor = vtkTextActor()
textActor.SetInput("Number Of iterations is :" + str(NUMBER_OF_ITERATIONS) + "\nNumber of Landmarks is:" + 
                   str(NUMBER_OF_LANDMARKS) + "\nTime Needed for matching:" + str(timeDifference) + " s")
textActor.GetTextProperty().SetFontSize(20)
textActor.SetPosition2(10,40)
textActor.GetTextProperty().SetColor(0.5,0.5,0.5)
###########################################

#Učitavanje scene
###########################################
realRenderer = vtkRenderer()
realRenderer.SetBackground(1.0, 1.0, 1.0)
realRenderer.AddActor(primaryActor)
realRenderer.AddActor(secondaryActor)
realRenderer.AddActor(theraryActor)

realRenderer.AddActor2D(textActor)


showingWindow = vtkRenderWindow()
showingWindow.SetSize(800, 600) #Veličina prozora na ekranu
showingWindow.SetWindowName("Scena") 
showingWindow.AddRenderer(realRenderer)
###########################################

#Postavljanje interactora za korisnički pregled 
###########################################
originalInteractor = vtkRenderWindowInteractor()
originalInteractor.SetRenderWindow(showingWindow)
originalInteractor.Initialize()
showingWindow.Render()
###########################################

#Iscrtavanje vektora poklapanja 
########################################### 
scalar_bar = vtkScalarBarActor()
scalar_bar.SetOrientationToHorizontal()
scalar_bar.SetLookupTable(lut)

scalar_bar_widget = vtkScalarBarWidget()
scalar_bar_widget.SetInteractor(originalInteractor)
scalar_bar_widget.SetScalarBarActor(scalar_bar)
scalar_bar_widget.On()
###########################################

#Prikaz prozora
###########################################
showingWindow.Render()
showingWindow.Render()
originalInteractor.Start() 
###########################################


print(timeDifference)
