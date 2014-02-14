#second part of face creation program
#places the points in boxes so you can compare the boxes with eachother?

import math
from math import *
import sys
import numpy

name_file_ply = 'outfile_new_points.ply'
file_ply = open(name_file_ply)
var_col = 0

#extracting the header
for x in range(0, 20):
    readheader = file_ply.readline().strip().split()
    if readheader[0] == 'end_header':
        var_header = x
    if 'red' in readheader:
        var_col += 1
    if 'blue' in readheader:
        var_col += 1
    if 'green' in readheader:
        var_col += 1
    if readheader[0] == "element" and readheader[1] == "vertex":
        var_vertex_ln = readheader[1]
        var_vertex_nm = readheader[2] #number of vertexen

    if readheader[0] == "element" and readheader[1] == "face":
        var_face_ln = readheader[1]
        var_face_nm = readheader[2]

listje = [] #sub list for coordinates
listtotal_vertex = [] #coordinates x,y,z list
listtotal_colors = []
sub_colors = []
print 'end header'
file_ply.close()
file1 = open(name_file_ply)

for a in range(0, (int(var_header) + int(var_vertex_nm) + int(var_face_nm) + 1)):
    line = file1.readline().strip().split()
    if int(var_header) < a < (int(var_vertex_nm)+ int(var_header)+1):
        rayx = listje.append(line[0])
        rayy = listje.append(line[1])
        rayz = listje.append(line[2])
        listtotal_vertex.append(listje) #x y z coordinates to list
        listje = []        

print 'end xyz coordinates to list'


#sort on y coordinaat
listtotal_vertex.sort(key = lambda x: float((x[1])))
#vertex with max y and vertex with min y 
lowest_y = float(listtotal_vertex[0][1]) #min y
highest_y = float(listtotal_vertex[-1][1]) #max y

#total number of points divided by the window of y
number_points_y_range = float(var_vertex_nm) / (highest_y - lowest_y)
print 'number of points in  y range: %s'%(number_points_y_range)
rangenm = float(var_vertex_nm)/ 1000000 #moet die 1000 zijn?
print 'rangenm', rangenm

#sort on x coordinate
listtotal_vertex.sort(key = lambda x: (float(x[0])))
lowest_x = float(listtotal_vertex[0][0])
highest_x = float(listtotal_vertex[-1][0])

print "lowest_x: %s"%(lowest_x)
print "highest_x: %s"%(highest_x)

# step sizes 
steps_y = (highest_y - lowest_y)/rangenm
steps_x = (highest_x - lowest_x)/rangenm
#print steps_x, 'steps_x'

#calculating number of boxes
number_of_boxes_hor = math.ceil(abs(highest_x/steps_x))
number_of_boxes_hor2 = math.ceil(abs(lowest_x/steps_x))
if number_of_boxes_hor < number_of_boxes_hor2:
    number_of_boxes_hor = number_of_boxes_hor2 # number of column boxes

number_of_boxes_ver = math.ceil(abs((highest_y + abs(lowest_y))/steps_y)) #number of row boxes



lijst_range = []
dictiolijst_co = {} #dictionary
x_start1 = 0.0
x_start2 = 0.0
x_window_max1 = 0.0
x_window_max2 = 0.0
y_window_min = lowest_y
y_window_max = lowest_y

#creating the dictionary with the varname as key and a empty list as value
for a in range(0,int(number_of_boxes_ver)): #number of rows
    for b in range(0, int((2*number_of_boxes_hor))): #number of columns
        varname = "%s_%s"%(a,b)
        dictiolijst_co[varname] = []


#filling the list with the varname and the x and y coordinates of the range.
# The varname exist of the row number of the box and the column number.
# Even column numbers are at the left site of the y axis, odd numbers at the right site.
for c in range(0,int(number_of_boxes_ver)):
    y_window_max += steps_y
    x_start1 = 0.0
    x_start2 = 0.0
    x_window_max1 = 0.0
    x_window_max2 = 0.0
    for d in range(0, int((2*number_of_boxes_hor))):
        varname = "%s_%s"%(c,d) #var name of the box
        if d%2 == 0: # even numbers, the left side of the object
            x_window_max1 += steps_x
            lijst_range.append([varname, x_start1, x_window_max1, y_window_min, y_window_max])
            x_start1 += steps_x
            
        else: #odd numbers, the right side of the object
            x_window_max2 -= steps_x
            lijst_range.append([varname, x_start2, x_window_max2, y_window_min, y_window_max])
            x_start2  -= steps_x
        #x_window_min += steps_x
    y_window_min += steps_y


# for loop to place al te coordinates in the right box
for f in range(0,len(listtotal_vertex)):
    x_point = float(listtotal_vertex[f][0]) #x coordinate face
    y_point = float(listtotal_vertex[f][1]) #y coordinate face 

    for g in range(0,len(lijst_range)):
        if x_point < 0: #if x is negative
            if  x_point <= float(lijst_range[g][1]) and x_point > float(lijst_range[g][2]):
                if y_point >= float(lijst_range[g][3]) and y_point < float(lijst_range[g][4]):
                    dictiolijst_co[str(lijst_range[g][0])].append(listtotal_vertex[f])
        else: # if x is positive
            if x_point >= float(lijst_range[g][1]) and x_point < float(lijst_range[g][2]):
                if y_point >= float(lijst_range[g][3]) and y_point < float(lijst_range[g][4]):
                    dictiolijst_co[str(lijst_range[g][0])].append(listtotal_vertex[f])
                

              
file1.close()
