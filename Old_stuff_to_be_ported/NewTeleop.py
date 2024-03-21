#!/usr/bin/env python3
"""
This node allows you to control the car with your pad
You are in a computer science school, you will understand this code without my help :)
"""
import serial
import os
from getkey import getkey, keys



HIGH_LIMIT_SPEED = 255
LOW_LIMIT_SPEED = 0
HIGH_LIMIT_ANG = 90
LOW_LIMIT_ANG = 0

SPEED_STEP = 1
ANGLE_STEP = 10

SPEED_LIMIT = 255
ANGLE_LIMIT = 90

class TeleopProg():


    def __init__(self):
        self.initial_state()

    #####################################

        # Recommend verbose : 2 for teleop | 1 for ai
        self.verbose = 1
        # Connecting to the arduino
        self.find_path_micro()
        self.baudrate = 115200
        self.arduino = serial.Serial(self.path_micro, self.baudrate, timeout=1)

        self.stm = serial.Serial()
        self.stm.port = self.path_micro
        self.stm.baudrate = self.baudrate
        self.linearSpeed=100
        self.angularPos=45
    
    ########################################
    
    def find_path_micro(self):
        """Find the USB port and initialyse it on self.path_micro"""
        print("Try to find USB path")
        for path in os.listdir("/dev"):
            if path[:-1] == "ttyUSB":
                self.path_micro = os.path.join("/dev/", path)
                print("USB path found : {}".format(self.path_micro))
                return
        self.print("Error : USB path not found")

    def rcv_order(self, order):
        if (order == "speed"):
            self.changePWMSpeed()
        elif (order == "angular"):
            self.changePWMDir()
        else:
            print("invalide type")





    ########################################
    
    def changePWMSpeed(self):
        order_type = 98
        arg = min(abs(self.linearSpeed), SPEED_LIMIT)
        self.sendOrder(98, arg)
        
    def changePWMDir(self):
        order_type = 97
        arg = (min(abs(self.angularPos), ANGLE_LIMIT))
        self.sendOrder(97, arg)
        
    def sendOrder(self, octet1: int, octet2: int):  # octet1 and octet2 should not be more that 8 bits
        trame = int.to_bytes((octet1 << 8) | octet2, 2, "big")
        self.arduino.write(trame)
    
    
    #########################################

    def initial_state(self):
        self.linearSpeed = 228
        self.angularPos = 45



    def read_key(self):
        res = True
        key = getkey()
        print(self.arduino.readline())
        

        #Speed control
        if (key == keys.UP):
            print("Accelerating"+str(self.linearSpeed + SPEED_STEP))
            self.linearSpeed += SPEED_STEP
            while (self.linearSpeed >= HIGH_LIMIT_SPEED) :
                print("reached limit")
                self.linearSpeed -= SPEED_STEP
            self.rcv_order("speed")
        elif (key == keys.DOWN):
            print("Slowing down"+str(self.linearSpeed - SPEED_STEP))
            self.linearSpeed -= SPEED_STEP
            while (self.linearSpeed <= LOW_LIMIT_SPEED) :
                print("reached limit")
                self.linearSpeed += SPEED_STEP
            self.rcv_order("speed")

        #Angle control
        elif (key == keys.RIGHT):
            print("Turning left"+str(self.angularPos + ANGLE_STEP))
            self.angularPos += ANGLE_STEP
            while self.angularPos >= HIGH_LIMIT_ANG :
                print("reached limit")
                self.angularPos -= ANGLE_STEP
            self.rcv_order("angular")
        elif (key == keys.LEFT):
            print("Turning right"+str(self.angularPos - ANGLE_STEP))
            self.angularPos -= ANGLE_STEP
            while self.angularPos <= LOW_LIMIT_ANG :
                print("reached limit")
                self.angularPos += ANGLE_STEP
            self.rcv_order("angular")

        elif (key == 'I'):
            print("linear speed:" + str(self.linearSpeed))
            print("angular position:" + str(self.angularPos))

        else :
            print("invalid key used")
        return res

    def main(self):
        cntn = True
        while cntn :
            cntn = self.read_key()

def main(args=None):
    prog = TeleopProg()
    prog.main()

if __name__ == '__main__':
    main()
