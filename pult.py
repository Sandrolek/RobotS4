#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pygame

import socket
import pickle

from config import *
from utils import *

#
FPS = 24
running = True

keys = []
power = 100

data = {
    'speedLeft' : power,
    'speedRight': power,
    'modeServo1': 0,
    'modeServo2': 0,
    'modeServo3': 0,
    'light' : 0
}

def Exit():
    pygame.quit()

pygame.init() 
pygame.mixer.quit() #

screen = pygame.display.set_mode([320, 240]) 
clock = pygame.time.Clock()

"""
#Joystick initialize

pygame.joystick.init() 
try:
    joy = pygame.joystick.Joystick(0)
    joy.init() 
    print('Enabled joystick: ' + joy.get_name())
except pygame.error:
    print('no joystick found.')
"""

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while running:
    cmd = ""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and "down" not in keys:
                keys.append("down")
            if event.key == pygame.K_UP and "up" not in keys:
                keys.append("up")
            if event.key == pygame.K_LEFT and "left" not in keys:
                keys.append("left")
            if event.key == pygame.K_RIGHT and "right" not in keys:
                keys.append("right")
            if event.key == pygame.K_a and "a" not in keys:
                keys.append("a")
            if event.key == pygame.K_z and "z" not in keys:
                keys.append("z")
            if event.key == pygame.K_s and "s" not in keys:
                keys.append("s")
            if event.key == pygame.K_x and "x" not in keys:
                keys.append("x")
            if event.key == pygame.K_d and "d" not in keys:
                keys.append("d")
            if event.key == pygame.K_c and "c" not in keys:
                keys.append("c")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                keys.remove("down")
            if event.key == pygame.K_UP:
                keys.remove("up")
            if event.key == pygame.K_LEFT:
                keys.remove("left")
            if event.key == pygame.K_RIGHT:
                keys.remove("right")
            if event.key == pygame.K_a:
                keys.remove("a")
            if event.key == pygame.K_z:
                keys.remove("z")
            if event.key == pygame.K_s:
                keys.remove("s")
            if event.key == pygame.K_x:
                keys.remove("x")
            if event.key == pygame.K_d:
                keys.remove("d")
            if event.key == pygame.K_c:
                keys.remove("c")
    if keys: 
        if 'up' in keys:
            data['speedLeft'] = -power
            data['speedRight'] = -power
        elif "down" in keys:
            data['speedLeft'] = power
            data['speedRight'] = power
        elif "left" in keys:
            data['speedLeft'] = -power
            data['speedRight'] = power
        elif "right" in keys:
            data['speedLeft'] = power
            data['speedRight'] = -power
        else:
            data['speedLeft'] = 0
            data['speedRight'] = 0

        data['modeServo1'] = 0
        data['modeServo2'] = 0
        data['modeServo3'] = 0
        if "a" in keys:
            data['modeServo1'] = 1
        if "z" in keys:
            data['modeServo1'] = -1
        if "s" in keys:
            data['modeServo2'] = -1
        if "x" in keys:
            data['modeServo2'] = 1
        if "d" in keys:
            data['modeServo3'] = 1
        if "c" in keys:
            data['modeServo3'] = -1
    else:
        data['speedLeft'] = 0
        data['speedRight'] = 0
        data['modeServo1'] = 0
        data['modeServo2'] = 0
        data['modeServo3'] = 0

    print("%s: speedLeft=%d, speedRight=%d, modeServo1=%d, modeServo2=%d, modeServo3=%d, light=%d" % (getDateTime(), data['speedLeft'], data['speedRight'], data['modeServo1'], data['modeServo2'], data['modeServo3'], data['light']))

    data1 = pickle.dumps(data)
    client.sendto(data1, (IP_BOARD, PORT_BOARD))

    pygame.display.update()         

    clock.tick(FPS)
        
Exit()

