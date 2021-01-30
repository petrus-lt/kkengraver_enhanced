#!/usr/bin/env python3
########################################################################
# Copyright 2019 Bernd Breitenbach
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>
#
########################################################################

# from engraver_B_b1 import main as laser
import sys
import os
# import subprocess
import time

global COM_port
global laser_matrix
laser_matrix = {}

def showComPortsAvailable():
    import serial.tools.list_ports
    for i in serial.tools.list_ports.comports():
        print(i) 

def laser(command):
    global COM_port
    #os.system('"python engraver_B_b2.py -d' + COM_port + ' -v ' + command +'"')
    os.system('"python engraver_B_b2.py -d' + COM_port + ' ' + command +'"')

# def laser_separate_window(command):
#     global COM_port
#     p = subprocess.Popen('t3.bat', creationflags=subprocess.CREATE_NEW_CONSOLE)

def show_laser_area(x, y):
    # laser('-H')   # HOME = python engraver_v4.py -d COM9 -v -H
    laser('-m ' + str(x) + 'mm:0mm')
    laser('-m 0:' + str(y) + 'mm')
    laser('-m " -' + str(x) + 'mm:0mm"')
    laser('-m " 0mm:-' + str(y) + 'mm"')
    
def calcDiagonalMatrix(tiles_per_dimension, width_of_tile, power_depth_delta):
    global laser_matrix
    #laser_matrix[0] = {'x': 0, 'y': 0, 'power': 10, 'depth': 10, 'path': '-m " ' + str(0) + 'mm:' + str(width_of_tile) + 'mm"'}
    current_element_nr = 0
    previous_element_nr = 0
    path = ''
    for y in range(tiles_per_dimension):
        for x in range(tiles_per_dimension):
            # print('current: x / y: {} / {}'.format(x, y))
            if x == (tiles_per_dimension-1):
                if y == (tiles_per_dimension-1):
                    path = '-m " -' + str((tiles_per_dimension-1) * width_of_tile) + 'mm:-' + str((tiles_per_dimension-1) * width_of_tile) + 'mm"'
                else:
                    path = '-m " -' + str(((tiles_per_dimension-2)-y) * width_of_tile) + 'mm:' + str(((tiles_per_dimension-1)-y) * width_of_tile) + 'mm"'
            elif y == 0:
                path = '-m " -' + str(x * width_of_tile) + 'mm:' + str((x+1) * width_of_tile) + 'mm"'
            else:
                path = '-m " ' + str(width_of_tile) + 'mm:-' + str(width_of_tile) + 'mm"'

            if x+y <= (tiles_per_dimension-1):    # top diagonal of matrix
                if x == 0:
                    # print('A')
                    current_element_nr = int(((y+1)/2)*y)
                    # print('x / y: {} / {}'.format(x, y))
                    # print('current_element_nr: ', current_element_nr)
                    # print('previous_element_nr: ', previous_element_nr)
                else:
                    # print('B')
                    current_element_nr = previous_element_nr + x + y + 1
                    # print('x / y: {} / {}'.format(x, y))
                    # print('current_element_nr: ', current_element_nr)
                    # print('previous_element_nr: ', previous_element_nr)
                laser_matrix[current_element_nr] = {'x': x, 'y': y, 'power': (x+1)*power_depth_delta, 'depth': (y+1)*power_depth_delta, 'path': path}
            else:           # bottom diagonal of matrix
                # print('c')
                current_element_nr = previous_element_nr - x - y + (2 * tiles_per_dimension)
                # print('x / y: {} / {}'.format(x, y))
                # print('current_element_nr: ', current_element_nr)
                # print('previous_element_nr: ', previous_element_nr)
                laser_matrix[current_element_nr] = {'x': x, 'y': y, 'power': (x+1)*power_depth_delta, 'depth': (y+1)*power_depth_delta, 'path': path}
            
            previous_element_nr = current_element_nr
    
    return laser_matrix

try: 
 
    global COM_port
    print('COM ports available')
    print('-------------------')
    showComPortsAvailable()
    COM_port_number = input('Please select COM port number [1 to 256]: ')
    try:
        COM_port_number = int(COM_port_number)
    except:
        None
    if isinstance(COM_port_number, int):
        if COM_port_number >= 1 and COM_port_number <= 256:
            COM_port = 'COM' + str(COM_port_number)
        else:
            print('COM port number not correct. Testing if COM9 is working')
            COM_port = 'COM9'            
    else:
        print('COM port number not correct. Testing if COM9 is working')
        COM_port = 'COM9'
    print('Port ' + COM_port + ' selected')
    
    home_choice = input('Do you want to home the laser [Y/n]?... ')
    if home_choice == 'y' or home_choice == 'Y' or home_choice == '':
        laser('-H')         # Home machine
        laser('--no-fan')    # Fan OFF

        
except Exception as e:
    print('Exception in TEST')
    print(e)

