# -*- coding: utf-8 -*-

import vtk
import math
 
#noninspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle 
#noninspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
 
from vtkmodules.vtkCommonMath import vtkMatrix4x4
from body import Body
from display import Display
#Iako to nije potrebno u ovoj funkciji predajemo dva parametra; prvi parametar 
#predstavlja osnovnu matricu odnosa odnosno matricu izmedu dva elementa bez rotacije
#drugi parametar predstavlja kut rotacije oko Z osi koji je potrebno prebaciti u radijane
#funkcija vraća matricu transformacije koja objedinjuje odnos lokacije i rotacije elemenata
def RotateJoint(MatricaOdnosa,theta):
    theta = (theta * 3.14)/180
    TForRotation= [
           math.cos(theta), 0,  math.sin(theta), 0.0,
            0, 1, 0, 0.0,
            -1* math.sin(theta), 0,math.cos(theta) , 0.0,
            0, 0, 0, 1.0
      ]
    TForReturn = [0]*16
    vtkMatrix4x4().Multiply4x4(MatricaOdnosa,TForRotation,TForReturn)
    return TForReturn 
    

def main():
    while True:
        try:
            theta1 = int(input("Enter 1st joint angle: ")) #Korisnik unosi tri kuta
            theta2 = int(input("Enter 2nd joint angle: ")) #koja predstavljaju kut rotacije 
            theta3 = int(input("Enter 3rd joint angle: ")) #valjaka odnosno zglobova
            
            theta4 = int(input("Enter 4th joint angle: "))
            break
        except:
            print("Syke, That's the wrong number")
            
    display = Display(500,500,"Test", 255,255,255) #Stvaramo prozor u kojem ćemo iscrtavati
    scene = Body()                                 #elemente s rotacijama pod određenim kutevima
    
    #################BOX1#########################
    
    Box1 = Body()
    Box1.CreateBox(0.4,0.4,0.15, 239,0,240)
    #KS baznog kvadra odnosno početni KS
    BaseMatrix = [
            1, 0, 0, 0.0,
            0, 1, 0, 0.0,
            0, 0, 1, 0.0,
            0, 0, 0, 1.0
      ] 
    Box1.Transform(BaseMatrix)
    ##############################################
    ################VALJAK1#######################
    
    Cylinder1 = Body()
    Cylinder1.CreateCylinder(0.025, 0.05, 50, 0, 232, 205)
    #KS prvog valjka odnosno predstavljanje lokacije valjka u odnosu na bazu
    FirstCylinderMatrix= [
            1, 0, 0, 0.0,
            0, 0, -1, 0.0,
            0, 1, 0, 0.10,
            0, 0, 0, 1.0
      ]
    #Pozivamo funkciju kojoj predajemo lokacijsku matricu te nam ona vraća 
    #Matricu homogene transformacije koja uključuje i rotaciju
    TRotated1 = RotateJoint(FirstCylinderMatrix, theta1)
    FirstCylinderTransformation = [0]*16
    #FirstCylinderTransformation predstavlja MHT za prvi zglob 
    vtkMatrix4x4().Multiply4x4(BaseMatrix,TRotated1,FirstCylinderTransformation)
    Cylinder1.Transform(FirstCylinderTransformation)
    ##############################################  
    ###############BOX2###########################
    
    Box2 = Body()
    Box2.CreateBox(0.4,0.1,0.1, 170,217,0)
    #KS drugog kvadra koji predstavlja lokaciju kvadra u odnosu na prvi zglob
    FirstHandLocationMatrix= [
            1, 0, 0, 0.15,
            0, 1, 0, 0.075,
            0, 0, 1, 0.0,
            0, 0, 0, 1.0
      ] 
    FirstHandTransformation = [0]*16
    #FirstHandTransformation predstavlja MHT prvog rotiranog kvadra (lokacija i rotacija)
    vtkMatrix4x4().Multiply4x4(FirstCylinderTransformation,FirstHandLocationMatrix,FirstHandTransformation)
    Box2.Transform(FirstHandTransformation)
    ##############################################
    ###############VALJAK2########################
    
    Cylinder2 = Body()
    Cylinder2.CreateCylinder(0.025, 0.05, 50, 0, 232, 205)
    #KS drugog valjka odnosno predstavljanje lokacije valjka u odnosu na prvi dio ruke(drugi kvadar)
    SecondCylinderMatrix= [
            1, 0, 0, 0.15,
            0, 1, 0, 0.075,
            0, 0, 1, 0.0,
            0, 0, 0, 1.0
      ] 
    #Pozivamo funkciju kojoj predajemo lokacijsku matricu te nam ona vraća 
    #Matricu homogene transformacije koja uključuje i rotaciju
    TRotated2 = RotateJoint(SecondCylinderMatrix, theta2)
    SecondCylinderTransformation = [0]*16
    #SecondCylinderTransformation predstavlja MHT za drugi zglob 
    vtkMatrix4x4().Multiply4x4(FirstHandTransformation,TRotated2,SecondCylinderTransformation)
    Cylinder2.Transform(SecondCylinderTransformation)
    ##############################################
    #############BOX3#############################
    
    Box3 = Body()
    Box3.CreateBox(0.4,0.1,0.1, 170,217,0)
    #KS treceg kvadra koji predstavlja lokaciju kvadra u odnosu na drugi zglob
    SecondHandLocationMatrix= [
            1, 0, 0, 0.15,
            0, 1, 0, 0.075,
            0, 0, 1, 0.0,
            0, 0, 0, 1.0
      ] 
    #SecondHandTransformation predstavlja MHT drugog rotiranog kvadra (lokacija i rotacija)
    SecondHandTransformation = [0]*16
    vtkMatrix4x4().Multiply4x4(SecondCylinderTransformation,SecondHandLocationMatrix,SecondHandTransformation)
    Box3.Transform(SecondHandTransformation)
    ##############################################
    ###############VALJAK3########################
    
    Cylinder3 = Body()
    Cylinder3.CreateCylinder(0.025, 0.05, 50, 0, 232, 205)
    ThirdCylinderMatrix= [
            1, 0, 0, 0.15,
            0, 1, 0, 0.075,
            0, 0, 1, 0.0,
            0, 0, 0, 1.0
      ] 
    #Pozivamo funkciju kojoj predajemo lokacijsku matricu te nam ona vraća 
    #Matricu homogene transformacije koja uključuje i rotaciju
    TRotated3 = RotateJoint(ThirdCylinderMatrix, theta3)
    ThirdCylinderTransformation = [0]*16
    #ThirdCylinderTransformation predstavlja MHT za treci zglob 
    vtkMatrix4x4().Multiply4x4(SecondHandTransformation,TRotated3,ThirdCylinderTransformation)
    Cylinder3.Transform(ThirdCylinderTransformation)
    ##############################################
    ###############BOX4###########################

    Box4 = Body()
    Box4.CreateBox(0.4,0.1,0.1, 170,217,0)
    ThirdHandLocationMatrix= [
            1, 0, 0, 0.15,
            0, 1, 0, 0.075,
            0, 0, 1, 0.0,
            0, 0, 0, 1.0
      ] 
    ThirdHandTransformation = [0]*16
    vtkMatrix4x4().Multiply4x4(ThirdCylinderTransformation,ThirdHandLocationMatrix,ThirdHandTransformation)
    Box4.Transform(ThirdHandTransformation)
    ##############################################
    
    
    ##############################################
    #                                            #
    #              BONUS PART!!!!!!              #
    #                                            #
    ##############################################
    
    ###############VALJAK4########################
    Cylinder4 = Body()
    Cylinder4.CreateCylinder(0.025, 0.05, 50, 0, 232, 205)
    FourthCylinderMatrix= [
             0, -1, 0, 0.225,
             1, 0, 0, 0.0,
             0, 0, 1, 0.0,
             0, 0, 0, 1.0
             ] 
    #Pozivamo funkciju kojoj predajemo lokacijsku matricu te nam ona vraća 
    #Matricu homogene transformacije koja uključuje i rotaciju
    TRotated4 = RotateJoint(FourthCylinderMatrix, theta4)
    FourthCylinderTransformation = [0]*16
    #FourthCylinderTransformation predstavlja MHT za cetvrti zglob 
    vtkMatrix4x4().Multiply4x4(ThirdHandTransformation,TRotated4,FourthCylinderTransformation)
    Cylinder4.Transform(FourthCylinderTransformation)
    ##############################################
    ###############BOX4###########################
    
    Box5 = Body()
    Box5.CreateBox(0.4,0.1,0.1, 170,217,0)
    FourthHandLocationMatrix= [
            1, 0, 0, -0.15,
            0, 1, 0, -0.075,
            0, 0, 1, 0.0,
            0, 0, 0, 1.0
            ] 
    FourthHandTransformation = [0]*16
    vtkMatrix4x4().Multiply4x4(FourthCylinderTransformation,FourthHandLocationMatrix,FourthHandTransformation)
    Box5.Transform(FourthHandTransformation)
    ##############################################
    #Dodavanje djelova u nasu scenu koju prikazujemo
    ##############################################
    scene.AddPart(Box1)
    scene.AddPart(Cylinder1)
    scene.AddPart(Box2)
    scene.AddPart(Cylinder2)
    scene.AddPart(Box3)
    scene.AddPart(Cylinder3)
    scene.AddPart(Box4)
    scene.AddPart(Cylinder4)
    scene.AddPart(Box5)
    scene.AddToDisplay(display)
    display.Run()
       
if __name__ == "__main__":
    main()
