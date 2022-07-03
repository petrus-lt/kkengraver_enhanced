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
    print('-----------------------------------------------------------------------------------------------') 
    print('|  KKMoon 3000mW laser test pattern program                                                   |')
    print('-----------------------------------------------------------------------------------------------\n') 
    ls_choice = input('Do you want to engrave with active laser [Y/n]?... ')
    if ls_choice == 'y' or ls_choice == 'Y' or ls_choice == '':
        laser_active_mode = True     # for testing: laser_active_mode = False  - for active engraving: laser_active_mode = True
        print('--> Laser will be used')
    else:
        laser_active_mode = False     # for testing: laser_active_mode = False  - for active engraving: laser_active_mode = True
        print('--> Laser will be deactivated and only dummy movements and drawing frames will be made')        
    # laser_active_mode = True     # for testing: laser_active_mode = False  - for active engraving: laser_active_mode = True
    
    
    global COM_port
    print('COM ports available')
    print('-------------------')
    showComPortsAvailable()
    COM_port_number = input('Please select COM port number [1 to 256] or tty device (complete path) : ')
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
        COM_port = COM_port_number
    print('Port ' + COM_port + ' selected')
    
    # laser('--fan')      # Fan ON 
    laser('--no-fan')    # Fan OFF
    
    
    # TEST1 = Power and Depth test (from 10% to 100% in 10% steps)
    # x = power axis
    # y = depth axis
    print('-----------------------------------------------------------------------------------------------') 
    print('|  Menu for testing laser engraver                                                            |')
    print('-----------------------------------------------------------------------------------------------') 
    print('Please select menu option:')
    print('')
    print('Engraving test pattern:')
    print('  A. Burn test pattern Power vs. Depth, 80x80mm, 10x10 tiles, 8x8mm per tile, in steps of 10%')
    print('  B. Burn test pattern Power vs. Depth, 40x40mm, 10x10 tiles, 4x4mm per tile, in steps of 10%')
    print('  C. Burn test pattern Power vs. Depth, 30x30mm, 10x10 tiles, 3x3mm per tile, in steps of 10%')
    print('  D. Burn test pattern Power vs. Depth, 40x40mm,   5x5 tiles, 8x8mm per tile, in steps of 20%')
    print('  E. Burn test pattern Power vs. Depth, 20x20mm,   5x5 tiles, 4x4mm per tile, in steps of 20%')
    print('')
    print('Cutting test pattern:')
    print('  1. Cut test pattern of 40x40mm size, 5x5 tiles, 8x8mm per tile, one more pass per tile, 1px cut line')
    print('  2. Cut test pattern of 40x40mm size, 5x5 tiles, 8x8mm per tile, one more pass per tile, 2px cut line')
    print('  3. Cut test pattern of 40x40mm size, 5x5 tiles, 8x8mm per tile, one more pass per tile, 3px cut line')    
    print('  4. Cut test pattern of 20x20mm size, 5x5 tiles, 4x4mm per tile, one more pass per tile, 1px cut line')
    print('  5. Cut test pattern of 20x20mm size, 5x5 tiles, 4x4mm per tile, one more pass per tile, 2px cut line')
    print('  6. Cut test pattern of 20x20mm size, 5x5 tiles, 4x4mm per tile, one more pass per tile, 3px cut line')    
    print('')
    print('  Q. Quit')
    print('')        
    
    menu_selection = input('> ')
    mode = 'none'
    if menu_selection == 'A' or menu_selection == 'a':
        mode = 'engrave'
        # depth = 10
        # power = 10
        delta = 10      # delta for power  and  delta for depth (step size from tile to tile)
        x_y_delta = 8   # in mm
        x_y_amount_tiles = 10
        laser('-H')         # Home machine
        laser('-F TEST1_background_80x80mm.png')
        engrave_image = 'TEST1_8x8mm.png'
    elif menu_selection == 'B' or menu_selection == 'b':
        mode = 'engrave'
        # depth = 20
        # power = 20
        delta = 10      # delta for power  and  delta for depth (step size from tile to tile)
        x_y_delta = 4   # in mm
        x_y_amount_tiles = 10
        laser('-H')         # Home machine
        laser('-F TEST1_background_40x40mm.png')
        engrave_image = 'TEST1_4x4mm.png'
    elif menu_selection == 'C' or menu_selection == 'c':  
        mode = 'engrave'
        # depth = 20
        # power = 20
        delta = 10      # delta for power  and  delta for depth (step size from tile to tile)
        x_y_delta = 3   # in mm
        x_y_amount_tiles = 10
        laser('-H')         # Home machine
        laser('-F TEST1_background_30x30mm.png')
        engrave_image = 'TEST1_3x3mm.png'
    elif menu_selection == 'D' or menu_selection == 'd':  
        mode = 'engrave'
        # depth = 20
        # power = 20
        delta = 20      # delta for power  and  delta for depth (step size from tile to tile)
        x_y_delta = 8   # in mm
        x_y_amount_tiles = 5
        laser('-H')         # Home machine
        laser('-F TEST1_background_40x40mm.png')
        engrave_image = 'TEST1_8x8mm.png'        
    elif menu_selection == 'E' or menu_selection == 'e':  
        mode = 'engrave'
        # depth = 20
        # power = 20
        delta = 20      # delta for power  and  delta for depth (step size from tile to tile)
        x_y_delta = 4   # in mm
        x_y_amount_tiles = 5
        laser('-H')         # Home machine
        laser('-F TEST1_background_20x20mm.png')
        engrave_image = 'TEST1_4x4mm.png'
    elif menu_selection == 'Z' or menu_selection == 'z':  
        mode = 'engrave'
        # depth = 20
        # power = 20
        delta = 33      # delta for power  and  delta for depth (step size from tile to tile)
        x_y_delta = 10   # in mm
        x_y_amount_tiles = 3
        laser('-H')         # Home machine
        laser('-F TEST1_background_20x20mm.png')
        engrave_image = 'TEST1_4x4mm.png'        
    elif menu_selection == '1':
        mode = 'cut'
        cutting_image = 'TEST2_cutting_8x8mm_1px.png'
        x_y_delta = 8   # in mm
        x_y_amount_tiles = 5
        delta = 20      # only needed for calcDiagonalMatrix() function         # delta for power and delta for depth (step size from tile to tile)
        laser('-H')         # Home machine
        laser('-F TEST1_background_40x40mm.png')
    elif menu_selection == '2':
        mode = 'cut'
        cutting_image = 'TEST2_cutting_8x8mm_2px.png'
        x_y_delta = 8   # in mm
        x_y_amount_tiles = 5
        delta = 20      # only needed for calcDiagonalMatrix() function         # delta for power and delta for depth (step size from tile to tile)
        laser('-H')         # Home machine
        laser('-F TEST1_background_40x40mm.png')
    elif menu_selection == '3':
        mode = 'cut'
        cutting_image = 'TEST2_cutting_8x8mm_3px.png'
        x_y_delta = 8   # in mm
        x_y_amount_tiles = 5
        delta = 20      # only needed for calcDiagonalMatrix() function         # delta for power and delta for depth (step size from tile to tile)
        laser('-H')         # Home machine
        laser('-F TEST1_background_40x40mm.png')        
    elif menu_selection == '4':
        mode = 'cut'
        cutting_image = 'TEST2_cutting_4x4mm_1px.png'
        x_y_delta = 4   # in mm
        x_y_amount_tiles = 5
        delta = 20      # only needed for calcDiagonalMatrix() function         # delta for power and delta for depth (step size from tile to tile)
        laser('-H')         # Home machine
        laser('-F TEST1_background_20x20mm.png')
    elif menu_selection == '5':
        mode = 'cut'
        cutting_image = 'TEST2_cutting_4x4mm_2px.png'
        x_y_delta = 4   # in mm
        x_y_amount_tiles = 5
        delta = 20      # only needed for calcDiagonalMatrix() function         # delta for power and delta for depth (step size from tile to tile)
        laser('-H')         # Home machine
        laser('-F TEST1_background_20x20mm.png')
    elif menu_selection == '6':
        mode = 'cut'
        cutting_image = 'TEST2_cutting_4x4mm_3px.png'
        x_y_delta = 4   # in mm
        x_y_amount_tiles = 5
        delta = 20      # only needed for calcDiagonalMatrix() function         # delta for power and delta for depth (step size from tile to tile)
        laser('-H')         # Home machine
        laser('-F TEST1_background_20x20mm.png')        
    elif menu_selection == '3':
        mode = 'cut'
        cutting_image = 'TEST2_cutting_4x4mm.png'
        x_y_delta = 10   # in mm
        x_y_amount_tiles = 3
        delta = 20      # only needed for calcDiagonalMatrix() function         # delta for power and delta for depth (step size from tile to tile)
        laser('-H')         # Home machine
        laser('-F TEST1_background_20x20mm.png')        
    else:
        sys.exit("Error: No valid value has been entered! Please try again.\nExiting script.")
        
        
    resume_choice = input("Do you want to use the previously selected area [y/N]?... ")
    if resume_choice == 'y' or resume_choice == 'Y':
        calcDiagonalMatrix(x_y_amount_tiles, x_y_delta, delta)
        if mode == 'engrave':
            laser('--fan')      # Fan ON
            # laser('-H')         # Home machine
            for i in range(len(laser_matrix)):
                print('engraving: x={}, y={}, power={}, depth={}, tile_number={}, path_to_next_tile={}'.format(laser_matrix[i]['x'], laser_matrix[i]['y'], laser_matrix[i]['power'], laser_matrix[i]['depth'], i+1, laser_matrix[i]['path']))
                if laser_active_mode: 
                    laser('-D ' + str(laser_matrix[i]['depth']) + ' -P ' + str(laser_matrix[i]['power']) + ' -i ' + engrave_image)      # burn image TEST1.png with depth and power set to the current loop values
                else:
                    time.sleep(0.5)
                laser(laser_matrix[i]['path'])      # get move command to move to next diagonal tile and perform the operation
        elif mode == 'cut':
            selected_power = input("Enter power output for cutting [0% to 100%, as integer]?... ")
            selected_depth = input("Enter cutting depth for cutting [0% to 100%, as integer]?... ")
            if int(selected_power) >= 0 and int(selected_power) <= 100 and int(selected_depth) >= 0 and int(selected_depth) <= 100:
                laser('--fan')      # Fan ON 
                # laser('-H')         # Home machine
                passes=1            # initial amount of cutting passes
                for y in range(x_y_amount_tiles):
                    for x in range(x_y_amount_tiles):
                        if x > 0:
                            laser('-m ' + str(x_y_delta) + 'mm:0mm')  # move laser in x direction only
                        for p in range(passes):
                            print('cutting: x={}, y={}, power={}, depth={}, passes={}'.format(x, y, selected_power, selected_depth, passes))
                            if laser_active_mode: 
                                laser('-D ' + str(selected_depth) + ' -P ' + str(selected_power) + ' -i ' + cutting_image)  # cut line
                            else:
                                time.sleep(0.5)
                        passes = passes + 1
                    if x == x_y_amount_tiles-1 and y == x_y_amount_tiles-1:
                        laser('-m " -' + str((x_y_amount_tiles-1)*x_y_delta) + 'mm:-' + str((x_y_amount_tiles-1)*x_y_delta) + 'mm"')    # move laser to home without using home command
                    else:
                        laser('-m " -' + str((x_y_amount_tiles-1)*x_y_delta) + 'mm:' + str(x_y_delta) + 'mm')  # move laser into new line of matrix
            else:
                print('Value for selected_power=' + str(selected_power) + 'or selected_depth=' + str(selected_depth) + ' is not correct. Please try again with values ranging from 0% to 100% as integer.')
    laser('-H')         # Home machine
        
except Exception as e:
    print('Exception in TEST')
    print(e)

