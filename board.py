#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import threading

import socket
import pickle

import RPiPWM

from config import *
from utils import *

def Exit():
    running = False
    server.close()
    print('The END')

curLights = 0

# !!!!!!!! на первой серве задаем частоту ШИМ канала для ВСЕХ ШИМ девайсов
modeServo1 = 0
modeServo2 = 0
modeServo3 = 0

servo1_180 = RPiPWM.Servo180(CH_SERVO1, extended=True, freq=RPiPWM.PwmFreq.H125)
servo2_180 = RPiPWM.Servo180(CH_SERVO2, extended=True)
servo3_180 = RPiPWM.Servo180(CH_SERVO3, extended=True)

print("Servo channels: Servo180_1 - %d, Servo180_2 - %d, Servo180_3 - %d" % (CH_SERVO1, CH_SERVO2, CH_SERVO3))

servo1_180.setMcs(SERVO_1_START)
servo2_180.setMcs(SERVO_2_START)
servo3_180.setMcs(SERVO_3_START)

# Порты моторов
chanRevMotorL = CH_LEFT
chanRevMotorR = CH_RIGHT

# создаем объекты моторов
motorL = RPiPWM.ReverseMotor(chanRevMotorL)
motorR = RPiPWM.ReverseMotor(chanRevMotorR)

def Motors(leftSpeed, rightSpeed):
    motorL.setValue(leftSpeed)
    motorR.setValue(rightSpeed)

class MotorsServo(threading.Thread):
    def __init__(self):
        super(MotorsServo, self).__init__()
        self.daemon = True
        self.interval = SERVO_INTERVAL
        self.stopped = threading.Event()

    def run(self):
        print('MotorsServo started')

        curServo1 = 0
        curServo2 = 0
        curServo3 = 0

        while not self.stopped.wait(self.interval):
            try:
                global modeServo1, modeServo2, modeServo3

                curServo1 = servo1_180.getValue()
                curServo2 = servo2_180.getValue()
                curServo3 = servo3_180.getValue()

                if (modeServo1 != 0 or modeServo2 !=0 or modeServo3 !=0):
                    print('Servo1 %d/%d, Servo2: %d/%d, Servo3: %d/%d' % (curServo1, modeServo1, curServo2, modeServo2, curServo3, modeServo3))

                if modeServo1 == 1:
                    curServo1 = curServo1 + STEP_1
                    if curServo1 > SERVO_1_MAX:
                        curServo1 = SERVO_1_MAX
                    servo1_180.setMcs(curServo1)
                elif modeServo1 == -1:
                    curServo1 = curServo1 - STEP_1
                    if curServo1 < SERVO_1_MIN:
                        curServo1 = SERVO_1_MIN
                    servo1_180.setMcs(curServo1)

                if modeServo2 == 1:
                    curServo2 = curServo2 + STEP_2
                    if curServo2 > SERVO_2_MAX:
                        curServo2 = SERVO_2_MAX
                    servo2_180.setMcs(curServo2)
                elif modeServo2 == -1:
                    curServo2 = curServo2 - STEP_2
                    if curServo2 < SERVO_2_MIN:
                        curServo2 = SERVO_2_MIN
                    servo2_180.setMcs(curServo2)

                if modeServo3 == 1:
                    curServo3 = curServo3 + STEP_3
                    if curServo3 > SERVO_3_MAX:
                        curServo3 = SERVO_3_MAX
                    servo3_180.setMcs(curServo3)
                elif modeServo3 == -1:
                    curServo3 = curServo3 - STEP_3
                    if curServo3 < SERVO_3_MIN:
                        curServo3 = SERVO_3_MIN
                    servo3_180.setMcs(curServo3)

            except Exception as err:
                print("%s MotorsServo: Error: %s" % (getDateTime(), err))

    def stop(self):
        self.stopped.set()

#     
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((IP_BOARD, PORT_BOARD))
print("Board started: %s on port %d..." % (IP_BOARD, PORT_BOARD))
server.settimeout(TIMEOUT)

motorsServo = MotorsServo()
motorsServo.start()

data_src = data_src_old = None

speedLeft = 0
speedRight = 0

running = True

while running:
    try:
        data_src = server.recvfrom(1024)
        
        if data_src != data_src_old:
            data_src_old = data_src

            data = pickle.loads(data_src[0])
        
            print("%s: speedLeft=%d, speedRight=%d, modeServo1=%d, modeServo2=%d, modeServo3=%d, light=%d" % (getDateTime(), data['speedLeft'], data['speedRight'], data['modeServo1'], data['modeServo2'], data['modeServo3'], data['light']))
            
            speedLeft = data['speedLeft']
            speedRight = data['speedRight']
            
            modeServo1 = data['modeServo1']
            modeServo2 = data['modeServo2']
            modeServo3 = data['modeServo3']
            
            Motors(speedLeft, speedRight)

    except socket.timeout:
        running = False
        print("Time is out...")

    except (KeyboardInterrupt, SystemExit):
        Exit()
        print("KeyboardInterrupt")

print("End program")
