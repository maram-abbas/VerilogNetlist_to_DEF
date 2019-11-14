#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 01:30:06 2019

@author: maramabbas
"""
import random

path = "sha1_core_synth.rtl.v"
pins = []

file = open(path, "r")
for i, line in enumerate(file):
    if line.find('input') != -1:
        line = line[len('input') + 1:line.find(';')]
        if line.find('[') == -1:
            pins.append(line)
        else:
            part_1 = int(line[line.find('[') + 1:line.find(':')])
            #print(part_1)
            part_2 = int(line[line.find(':') + 1:line.find(']')])
            part_3 = part_1 + part_2
            word = line[line.find(' ') + 1:]
            #print(word)
            for j in range(part_3 + 1):
                pins.append(word + '<' + str(j) + '>')
                
    elif line.find('output') != -1:
        line = line[len('output') + 1:line.find(';')]
        if line.find('[') == -1:
            pins.append(line)
        else:
            part_1 = int(line[line.find('[') + 1:line.find(':')])
            #print(part_1)
            part_2 = int(line[line.find(':') + 1:line.find(']')])
            part_3 = part_1 + part_2
            word = line[line.find(' ') + 1:]
            #print(word)
            for j in range(part_3 + 1):
                pins.append(word + '<' + str(j) + '>')
                
    elif line.find('module') != -1 and line.find('endmodule') == -1:
        module_name = line[line.find('module') + len('module '):line.find(' ',len('module '))]
    #print(line)
                
file.close()                
#print(pins)

file = open(module_name + "_pins.txt","w+")

sides = ['L','R','U','D']
metal = ''

for p in pins:
    i = random.randint(0,3)
    j = random.randint(0,1)
    if i == 0 or i == 1:
        if j == 1:
            metal = 'M1'
        else:
            metal = 'M3'
    else:
        if j == 1:
            metal = 'M2'
        else:
            metal = 'M4'
    file.write(p + '\t' + sides[i] + '\t' + metal + '\n')
    #print(p)
file.close()

        
                
                
                
            
            