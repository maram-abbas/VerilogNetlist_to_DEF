#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 20:45:29 2019

@author: maramabbas
"""
from lef_util import *
from util import *
import math
import random

SCALE = 2000

class LefParser:
    """
    LefParser object will parse the LEF file and store information about the
    cell library.
    """
    def __init__(self, lef_file):
        self.lef_path = lef_file
        # dictionaries to map the definitions
        self.macro_dict = {}
        self.layer_dict = {}
        self.via_dict = {}
        # can make the stack to be an object if needed
        self.stack = []
        # store the statements info in a list
        self.statements = []
        self.cell_height = -1

    def get_cell_height(self):
        """
        Get the general cell height in the library
        :return: void
        """
        for macro in self.macro_dict:
            self.cell_height = self.macro_dict[macro].info["SIZE"][1]
            #print (self.cell_height)
            break

    def parse(self):
        # Now try using my data structure to parse
        # open the file and start reading
        #print ("Start parsing LEF file...")
        f = open(self.lef_path, "r")
        # the program will run until the end of file f
        for line in f:
            #print (line)
            info = str_to_list(line)
            #print (info)
            if len(info) != 0:
                # if info is a blank line, then move to next line
                # check if the program is processing a statement
                #print (info)
                if len(self.stack) != 0:
                    curState = self.stack[len(self.stack) - 1]
                    #print (curState)
                    nextState = curState.parse_next(info)
                    #print (nextState)
                else:
                    curState = Statement()
                    nextState = curState.parse_next(info)
                # check the status return from parse_next function
                if nextState == 0:
                    # continue as normal
                    pass
                elif nextState == 1:
                    # remove the done statement from stack, and add it to the statements
                    # list
                    if len(self.stack) != 0:
                        # add the done statement to a dictionary
                        done_obj = self.stack.pop()
                        if isinstance(done_obj, Macro):
                            self.macro_dict[done_obj.name] = done_obj
                        elif isinstance(done_obj, Layer):
                            self.layer_dict[done_obj.name] = done_obj
                        elif isinstance(done_obj, Via):
                            self.via_dict[done_obj.name] = done_obj
                        self.statements.append(done_obj)
                elif nextState == -1:
                    pass
                else:
                    self.stack.append(nextState)
                    # print (nextState)
        f.close()
        # get the cell height of the library
        #self.get_cell_height()
        #print ("Parsing LEF file done.")

class VNetParser:
    
    """
    VNetParser object will parse the verilog netlist file 
    """
    
    def __init__(self, vnet_file):
        #ALL LISTS HAVE SAME ORDER OF OCCURANCE IN .V FILE
        self.vnet_path = vnet_file
        self.pins = []
        self.declared_wires = []
        self.values_of_declared_wires = [] #same order as declared_wires
        self.undeclared_wires = []
        self.cell_name = []
        self.called_cell_name = [] #same order as cell_name
        self.cell_pins = []
        self.pins_wires_all_nets = []
        self.instance_of_cell_pins = []
        self.where_am_i = 0
        self.flag = 0
        self.flag3 = 0
        
    def parse(self):
        file = open(self.vnet_path, "r")
        for i, line in enumerate(file):
            if line:
                if i != 0 and line != '\n' and line != 'endmodule\n':
                    if line.find('input') != -1:  #handling pins
                        if line.find('[') == -1:
                            self.pins.append(line[6:len(line) - 2])
                            #print(line)
                        else:
                            index_1 = line.find('[')
                            index_2 = line.find(':')
                            index_3 = line.find(']')
                            var_name = line[index_3 + 2:line.find(';')]
                            max_bus = line[index_1 + 1: index_2]
                            for a in range(0, int(max_bus) + 1):
                                self.pins.append(var_name + "<" + str(a) + ">")
                    elif line.find('output') != -1:
                        if line.find('[') == -1:
                            self.pins.append(line[7:len(line) - 2])
                            #print(line)
                        else:
                            index_1 = line.find('[')
                            index_2 = line.find(':')
                            index_3 = line.find(']')
                            var_name = line[index_3 + 2:line.find(';')]
                            max_bus = line[index_1 + 1: index_2]
                            for a in range(0, int(max_bus) + 1):
                                self.pins.append(var_name + "<" + str(a) + ">")
                    elif line.find('wire') != -1:           #handling wires
                        if line.find('[') == -1:
                            first_space = line.find(' ')
                            second_space = line.find(' ', first_space + 1, len(line))
                            self.declared_wires.append(line[first_space + 1: second_space])
                        
                            index_1 = line.find('=')
                            self.values_of_declared_wires.append(line[index_1 + 5: index_1 + 6])
                        #else:
                            #write code that supports busses
                    else:   #handling calling of functions
                        self.where_am_i = self.where_am_i + 1
                        self.flag = 1
                        self.flag3 = 1
                        first_space = line.find(' ')
                        second_space = line.find(' ', first_space + 1, len(line))
                        self.cell_name.append(line[0:first_space])
                        self.called_cell_name.append(line[first_space + 1: second_space])
                        count = 0
                        count2 = 0
                        count_dot = 0
                        flag2 = 0
                        for elem in line:
                            flag2 = 0
                            count2 = count2 + 1
                            if elem == '(':
                                count = count + 1
                                if count != 1:
                                    #c = c + 1
                                    paran_1 = line.find('(', count2 - 1)
                                    paran_2 = line.find(')', paran_1)
                                    if self.flag == 1: # so no empty appends done
                                        self.cell_pins.append([]) #making it 2D
                                        self.flag = 0
                                    param = line[paran_1 + 1:paran_2]
                                    #print(param)
                                    if param.find('[') != -1:
                                        param = param.replace('[','<')
                                        param = param.replace(']','>')
                                        #print(param)
                                    first_ = param.find('_');
                                    if first_ != -1:
                                        check = 0
                                        second_ = param.find('_', first_ + 1)
                                        if second_ == -1:
                                            param = param.replace('_','.')
                                            for item in self.undeclared_wires:
                                                #print(item)
                                                if item == param:
                                                    check = 1
                                        for item in self.undeclared_wires:
                                                #print(item)
                                                if item == param:
                                                    check = 1
                                        if check == 0:
                                            self.undeclared_wires.append(param)
                                    self.cell_pins[self.where_am_i - 1].append(param)
                                    for item in self.pins_wires_all_nets:
                                        #print(item)
                                        #print(param)
                                        if item == param:
                                            flag2 = 1
                                            #print("YESS")
                                    if flag2 == 0:
                                        self.pins_wires_all_nets.append(param)
                                        #print(self.pins_wires_all_nets)
                            
                            if elem == '.':
                                if self.flag3 == 1: # so no empty appends done
                                    self.instance_of_cell_pins.append([]) #making it 2D
                                    self.flag3 = 0
                                dot_place = line.find('.',count2 - 1)
                                paran_after = line.find('(',count2 - 1)
                                inst = line[dot_place + 1:paran_after]
                                #print(inst)
                                self.instance_of_cell_pins[self.where_am_i - 1].append(inst)
                
        file.close()
                           

class PinsParser:
    
    """
    PinsParser object will parse the text file containing information about the pins 
    """  
           
    def __init__(self, pins_file):
        self.pins_path = pins_file
        self.pins = []
        self.side = []
        self.metal_layer = []
    
    def parse(self):
        file = open(self.pins_path, "r")
        for line in file:
            if line:
                first_tab = line.find('\t')
                self.pins.append(line[:first_tab])
                second_tab = line.find('\t', first_tab + 1)
                self.side.append(line[first_tab + 1:second_tab])
                self.metal_layer.append(line[second_tab + 1:len(line) - 1])
        #print(self.pins)
        #print(self.side)
        #print(self.metal_layer)
                    
                                
if __name__ == '__main__':
    path_v = input("Enter verilog netlist file: ")
    #path_v = "rca4.rtlnopwr.v"
    #path_v = "mux4x1.rtlnopwr.v"
    #path_v = "test_5.rtlnopwr.v"
    vnet_parser = VNetParser(path_v)
    vnet_parser.parse()
    
    design = path_v[:path_v.find('.')]
    
    path_lef = input("Enter LEF file: ")
    #path_lef = "osu035_stdcells.lef"
    lef_parser = LefParser(path_lef)
    lef_parser.parse()
    
    path_pins = input("Enter pins file: ")
    #path_pins = "rca4_pins.txt"
    #path_pins = "mux4x1_pins.txt"
    #path_pins = "test_5_pins.txt"
    pins_parser = PinsParser(path_pins)
    pins_parser.parse()
    
    utilization = input("Enter utilization: ")
    aspect_ratio = input("Enter aspect_ratio: ")
    
    distance_microns = 100
    
    #REQUIRED STUFF
    nets = vnet_parser.pins_wires_all_nets
    pins = vnet_parser.pins
    cell_pins = vnet_parser.cell_pins
    called_cell_name = vnet_parser.called_cell_name
    instance_of_cell_pins = vnet_parser.instance_of_cell_pins
    cell_name = vnet_parser.cell_name
    
    #GETTING CORE AREA
    core_width = 0
    core_height = 0
    core_area = 0
    cells_area = 0
    utilization = 0.85     #input by user
    aspect_ratio = 1    #input by user
    #utilization = float(utilization)
    #aspect_ratio = float(aspect_ratio)
        
    #GET CELLS AREA FIRST
    area_of_each_cell = []
    for cell in cell_name:
        #print (cell)
        sp_cell = lef_parser.macro_dict[cell]
        area_of_each_cell.append(sp_cell.info["SIZE"][0] * sp_cell.info["SIZE"][1] * distance_microns * distance_microns)
            
    for new_area in area_of_each_cell:
        cells_area = cells_area + new_area
    
            
    #print(cells_area)
    
    core_width = math.sqrt((cells_area)/(utilization * aspect_ratio))
    
    core_height = aspect_ratio * core_width
    
    temp = core_width % 160
    if temp != 0:
        temp2 = 160 - temp
        core_width = core_width + temp2
        
    #print(lef_parser.get_cell_height())
    
    cell_height = int(lef_parser.cell_height) * distance_microns
    temp = core_height % cell_height
    if temp != 0:
        temp2 = cell_height - temp
        core_height = core_height + temp2
        
    #print(core_width % 160)
    #print(core_height % -cell_height)
    
    core_area = core_width * core_height

    def_file = open(design + ".def","w+")
    
    #HEADER
    def_file.write('VERSION 5.6 ;\nNAMESCASESENSITIVE ON ;\nDIVIDERCHAR "/" ;\nBUSBITCHARS "<>" ;\nDESIGN ' + design + ' ;\nUNITS DISTANCE MICRONS ' + str(distance_microns) + ' ;\n\n')
    
    #DIEAREA
    factor_x = len(pins) * 400
    factor_y = len(pins) * 400
    start_x = -480
    start_y = -400
    
    begin_x = start_x + factor_x
    begin_y = start_y + factor_y
    cell_height = lef_parser.cell_height * distance_microns  #getting cell height
    
    end_x = math.floor(start_x + factor_x + core_width + factor_x)
    end_y = math.floor(start_y + factor_y + core_height + factor_y)
    
    def_file.write('DIEAREA ( ' + str(start_x) + ' ' + str(start_y) + ' ) ( ' + str(end_x) + ' ' + str(end_y) + ' ) ;\n\n')
    
    #TRACKS
    for n in range(1,5):
        if n % 2 == 1:
            st = start_y
            en = end_y
        else:
            st = start_x
            en = end_x
            
        step = lef_parser.layer_dict["metal" + str(n)].pitch * distance_microns
        
        direction = lef_parser.layer_dict["metal" + str(n)].direction
        if direction == "HORIZONTAL":
            t = "Y"
        elif direction == "VERTICAL":
            t = "X"
        
        num = (((-st) + en) / int(step)) + 1
        def_file.write("TRACKS " + t + " " + str(st) + " DO " + str(int(num)) + " STEP " + str(int(step)) + " LAYER metal" + str(n) + " ;\n")
        
    def_file.write("\n")
    
    #COMPONENTS
    def_file.write("COMPONENTS " + str(len(called_cell_name)) + " ;\n")
    
    for i,elem in enumerate(called_cell_name):
        def_file.write("- " + elem + " " + cell_name[i] + " + PLACED ( 0 0 ) ; \n")
                
    def_file.write("END COMPONENTS\n\n")

    #PINS
    pins_file = pins_parser.pins
    side = pins_parser.side
    metal_layer = pins_parser.metal_layer
    
    for i,elem in enumerate(metal_layer):
        if elem == "M1":
            metal_layer[i] = "metal1"
        elif elem == "M2":
            metal_layer[i] = "metal2"
        elif elem == "M3":
            metal_layer[i] = "metal3"
        elif elem == "M4":
            metal_layer[i] = "metal4"
    
    def_file.write("PINS " + str(len(pins)) + " ;\n")
    
    new_index_M1_y = begin_y
    new_index_M3_y = begin_y
    new_index_M2_x = begin_x
    new_index_M4_x = begin_x
    
    for i,elem in enumerate(pins_file):
        
        step_M1 = lef_parser.layer_dict["metal1"].pitch * distance_microns
        
        step_M3 = lef_parser.layer_dict["metal3"].pitch * distance_microns
        
        step_M2 = lef_parser.layer_dict["metal2"].pitch * distance_microns
        
        step_M4 = lef_parser.layer_dict["metal4"].pitch * distance_microns
        
        check_if_used = 0
        def_file.write("- " + elem + " + NET " + elem + "\n")
        def_file.write("  + LAYER " + metal_layer[i] + " ( 0 0 ) ( 1 1 )\n")
        
        if side[i] == "L":
            #print("here")
            #print(metal_layer[i])
            if metal_layer[i] == "metal1":
                #print("lol")
                def_file.write("  + PLACED ( " + str(start_x) + " " + str(int(new_index_M1_y)) + " ) N ;\n")
                new_index_M1_y = new_index_M1_y + step_M1
            elif metal_layer[i] == "metal3":
                def_file.write("  + PLACED ( " + str(start_x) + " " + str(int(new_index_M3_y)) + " ) N ;\n")
                new_index_M3_y = new_index_M3_y + step_M3
                
        elif side[i] == "R":
            
            if metal_layer[i] == "metal1":
                def_file.write("  + PLACED ( " + str(end_x) + " " + str(int(new_index_M1_y)) + " ) N ;\n")
                new_index_M1_y = new_index_M1_y + step_M1
            elif metal_layer[i] == "metal3":
                def_file.write("  + PLACED ( " + str(end_x) + " " + str(int(new_index_M3_y)) + " ) N ;\n")
                new_index_M3_y = new_index_M3_y + step_M3
                
        elif side[i] == "U":
            
            if metal_layer[i] == "metal2":
                def_file.write("  + PLACED ( " + str(int(new_index_M2_x)) + " " + str(start_y) + " ) N ;\n")
                new_index_M2_x = new_index_M2_x + step_M2
            elif metal_layer[i] == "metal4":
                def_file.write("  + PLACED ( " + str(int(new_index_M4_x)) + " " + str(start_y) + " ) N ;\n")
                new_index_M4_x = new_index_M4_x + step_M4
                
        elif side[i] == "D":
            
            if metal_layer[i] == "metal2":
                def_file.write("  + PLACED ( " + str(int(new_index_M2_x)) + " " + str(end_y) + " ) N ;\n")
                new_index_M2_x = new_index_M2_x + step_M2
            elif metal_layer[i] == "metal4":
                def_file.write("  + PLACED ( " + str(int(new_index_M4_x)) + " " + str(end_y) + " ) N ;\n")
                new_index_M4_x = new_index_M4_x + step_M4
       
    def_file.write("END PINS\n\n")    
    
    #NETS
    def_file.write("NETS " + str(len(nets)) + " ;\n")
    
    for elem in nets:
        check = 0
        found = []
        found2 = []
        found_again = []
        count = 0
        
        def_file.write("- " + elem + "\n")          
        
        for row in range(len(cell_pins)):
            for p in range(len(cell_pins[row])):
                if cell_pins[row][p] == elem:
                    found.append(row)
                    found2.append(p)
        for item in pins:
            if item == elem:
                #print(item)
                #print(elem)
                def_file.write("  ( PIN " + elem + " )\n")
                
        #print(found2[0])
        for row in reversed(found):
            #print(row)
            count = 0
            called = called_cell_name[row]
            #print(called)
            
            for c in range(len(called_cell_name)):
                if called == called_cell_name[c]:
                    found_again = c
            #print(found_again)
            #print(instance_of_cell_pins[12][2])
            #print(found2)
            for row2 in reversed(found2):
                #print(row2)
                count = count + 1
                if count <= 1:
                    def_file.write("  ( " + called_cell_name[row] + " " + instance_of_cell_pins[found_again][found2[-1]] + " )")
            
            if row == found[0]:
                def_file.write(" ;\n")
            else:
                def_file.write("\n")
            del found2[-1]
            #print(count)  
    def_file.write("END NETS\n\nEND DESIGN") 
                    
    def_file.close()