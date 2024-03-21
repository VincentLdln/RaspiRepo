#### This program handles the servo and the motor through the arduino through Serial Terminal ####

import serial
import os


Speed_Limit=255
Angle_Limit=90

Speed_Step=1
Angle_Step=10

CarDir=45
CarSpeed=100

######################################################

def find_path_micro():
    """Find the USB port and initialyse it on self.path_micro"""
    print("Try to find USB path")
    for path in os.listdir("/dev"):
        if path[:-1] == "ttyUSB":
            path_micro=os.path.join("/dev/", path)
            print("USB path found : {}".format(path_micro))
            return
        print("Error : USB path not found")

path_micro=find_path_micro()

#######################################################

def changePWMSpeed(linearSpeed):
    order_type=98
    arg=min(abs(linearSpeed), Speed_Limit)
    sendOrder(order_type,arg)

def changePWMDir(anglePos):
    order_type=97
    arg=(min(abs(angularPos),Angle_Limit))
    sendOrder(order_type,arg)

#######################################################    

baudrate = 115200
arduino = serial.Serial(path_micro, baudrate, timeout=1)

def SendOrder(octet1,octet2):
    trame = int.to_bytes((octet1 << 8) | octet2, 2, "big")
    arduino.write(trame)

########################################################

def Accelerate(StepAmount=1):
    for _ in range StepAmount:
        if CarSpeed+Speed_Step<=Speed_Limit:
            CarSpeed+=Speed_Step
    changePWMSpeed(CarSpeed)

def Deccelerate(StepAmount=1):
    for _ in range StepAmount:
        if CarSpeed-Speed_Step>=0:
            CarSpeed-=Speed_Step
    changePWMSpeed(CarSpeed)

def TurnLeft(StepAmount=1):
    for _ in range StepAmount:
        if CarDir-Angle_Step>=0:
            CarDir-=Angle_Step
    changePWMDir(CarDir)

def TurnRight(StepAmount=1):
    for _ in range StepAmount:
        if CarDir+Angle_Step<=Angle_Limit:
            CarDir+=Angle_Step
    changePWMDir(CarDir)

########################################################
