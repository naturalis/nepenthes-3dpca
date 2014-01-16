#rotation version 2

import math
from math import *
import sys
file_name = raw_input("file: ")
#file_name = 'curvation_lower.dta'

#file_connect = raw_input("file: ")
#file_connect= 'mirror.txt'
#file_name = 'dart_landmark.dta'
#file_connect = raw_input("file: ")
file_connect= 'mirror.txt'

#maken dat die connect file onthoud. 

file_outputname = 'outputrotate.dta'
file_outputname2 = 'outputrotate2.dta'
file_outputname3 = 'outputrotate3.dta'
file_outputname4 = 'outputrotate4.dta'
file_outputname5 = 'outputcorrected.dta'
output = open(file_outputname, 'w')
output2 = open(file_outputname2, 'w')
output3 = open(file_outputname3, 'w')
output4 = open(file_outputname4, 'w')
output5 = open(file_outputname5, 'w')
while True:
    site = raw_input("left site is good:(Yes or No):  ").upper().strip()
    site.strip()
    if site == 'YES' or site == 'Y':
        site = 0
        break
    elif site == 'NO' or site == 'N':
        site = 1
        break
    else:
        print 'not the right input, try again'
datapoints = open(file_name)
datalines = datapoints.readlines()
listdata = []
listdta = []
sublistje = []

# open dta file
for a  in range(0,len(datalines)):
    aline = datalines[a].strip()
    listdta.append(datalines[a].strip().split('  ')) # let op spatie

    if len(listdta[a]) == 3:
        sublistje.append(float(listdta[a][0]))
        sublistje.append(float(listdta[a][1]))
        sublistje.append(float(listdta[a][2]))
        listdata.append(sublistje)
        sublistje = []
    else:
        output.write("%s\n"%(aline))
#print listdata

# open mirrorpoints file
mirrorpoints = open(file_connect)
lines= mirrorpoints.readlines()

listje = []
listjesym = []
for x in range(0, len(lines)):
    line = lines[x].strip()
    if line == 'sym':
        for a in range(1,4):
            listjesym.append(lines[a].strip().split())
    if line == 'mirror':
        for y in range(x + 1,len(lines)):
            listje.append(lines[y].strip().split())
#print 'sym', listjesym


sym1 = int(listjesym[0][0]) -1
sym2 = int(listjesym[1][0]) -1 
sym3 = int(listjesym[2][0]) -1


#shift to zeropoint ##########################################################

zeropoint = int(sym3)
co_zeropoint = listdata[zeropoint]

listdata2 = []
listdata3 = []
# minus x,y,z of point shift to zeropoint of every point
for x in range(0,len(listdata)):
    listdata2.append(listdata[x][0] - co_zeropoint[0])
    listdata2.append(listdata[x][1] - co_zeropoint[1])
    listdata2.append(listdata[x][2] - co_zeropoint[2])
    listdata3.append(listdata2)
    listdata2 = []

print 'listdata3', listdata3

for x in range(0,len(listdata)):
    output.write("%s %s %s\n"%(listdata3[x][0], listdata3[x][1], listdata3[x][2]))
output.close()


###################################################################################################################################################### 

def Rz_matrix(z_angle): # Rz rotation matrix
    return [[cos(math.radians(z_angle)), -sin(math.radians(z_angle)), 0.0],[sin(math.radians(z_angle)),cos(math.radians(z_angle)),0.0],[0.0, 0.0, 1.0]]


def Z_rotation(point2, z_angle): # multiplication rotation matrix and coordinates 
    r_z = Rz_matrix(z_angle)
    rotated_z = []               
    for i in range(3):
        rotated_z.append((sum([r_z[i][j] * point2[j] for j in range(3)])))
    return rotated_z


def Rx_matrix(x_angle): #rotation matrix x-axis
    return [[1, 0, 0],[0,cos(math.radians(x_angle)),-sin(math.radians(x_angle))],[0,sin(math.radians(x_angle)),cos(math.radians(x_angle))]]

def X_rotation(point3, x_angle): #multiplication rotation matrix and coordinates 
    r_x = Rx_matrix(x_angle)
    rotated_x = []  
    for i in range(3):
        rotated_x.append((sum([r_x[i][j] * point3[j] for j in range(3)])))
    return rotated_x


def Ry_matrix(y_angle): # Ry rotation matrix
    return [[cos(math.radians(y_angle)), 0.0, sin(math.radians(y_angle))],[0.0, 1.0, 0.0],[-sin(math.radians(y_angle)),0.0, cos(math.radians(y_angle))]]

def Y_rotation(point4, y_angle): #multiplication rotation matrix and coordinates 
    r_y = Ry_matrix(y_angle)
    rotated_y = []
    for i in range(3):
        rotated_y.append((sum([r_y[i][j] * point4[j] for j in range(3)])))
    return rotated_y


#########################################################################################################################################################


# als punt 13 onder punt 15 ligt, moet die 180 graden gedraaid worden over de z as maak eerst temp
listdatatemp = []
if listdata3[sym1][1] < listdata3[sym3][1]:
    print 'iets'
    angle = 180
    for coordinates in range(0,len(listdata3)):
        listdatatemp.append(Z_rotation(listdata3[coordinates], angle))
    print 'temp', listdatatemp
    listdata3 = listdatatemp
print listdata3

# Rotate around z axis ########################################################################

# calculate angle rotation
len_z_a = listdata3[int(sym1)][0] - listdata3[int(sym3)][0]
len_z_b = listdata3[int(sym1)][1] - listdata3[int(sym3)][1]

z_angle = (math.degrees(math.atan(len_z_a/len_z_b)))
print 'angle1',z_angle

# calculate new coordinates
listdata4 = []

for coordinates in range(0, len(listdata3)):
    #print 'r', Rotate2(listdata3[d], angle)
    listdata4.append(Z_rotation(listdata3[coordinates], z_angle))
print 'list4', listdata4

for x in range(0,len(listdata)):
    output2.write("%.7f %.7f %.7f\n"%(listdata4[x][0], listdata4[x][1], listdata4[x][2]))

output2.close()

# around x-axis ##############################################################################

#calculate angle point 13z / point 13y int(sym1)][0]
len_x_a = listdata4[int(sym1)][2] - listdata4[int(sym3)][0]
len_x_b = listdata4[int(sym1)][1] - listdata4[int(sym3)][0]
x_angle = -(math.degrees(math.atan(len_x_a/len_x_b))) # waarom hier een min voor?
print 'angle2', x_angle
listdata5 = []

# new coordinates in list
for d in range(0, len(listdata3)):
    #print 's', X_rotation(listdata4[d], x_angle)
    listdata5.append(X_rotation(listdata4[d], x_angle))

print 'listdata5', listdata5
# write new coordinates
for x in range(0,len(listdata)):
    output3.write("%.7f %.7f %.7f\n"%(listdata5[x][0], listdata5[x][1], listdata5[x][2]))


# Rotate around y axis#############################################################

#calculate angle 4 x coordinate point 3 / z coordinate point 3.
len_y_a = (listdata5[int(sym2)][0] - listdata5[int(sym3)][0])
len_y_b = (listdata5[int(sym2)][2] - listdata5[int(sym3)][2])
y_angle = -(math.degrees(math.atan(len_y_a/len_y_b)))
print 'angle3', y_angle
listdata6 = []

# new coordinates in list
for d in range(0, len(listdata5)):
    #print 's', Y_rotation(listdata5[d], y_angle)
    listdata6.append(Y_rotation(listdata5[d], y_angle))

print 'listdata6', listdata6

listdatatemp = []
if listdata6[sym1][2] < listdata6[sym3][1]:
    print 'iets2'
    angle = 180
    for coordinates in range(0,len(listdata6)):
        listdatatemp.append(Y_rotation(listdata6[coordinates], angle))
    print 'temp', listdatatemp
    listdata6 = listdatatemp
print 'listnew', listdata6

# write new coordinates
for x in range(0,len(listdata5)):
    output4.write("%.7f %.7f %.7f\n"%(listdata6[x][0], listdata6[x][1], listdata6[x][2]))


    
####################################################################################################################################################

#marge = 300 ####### hoe zouden we hier een getal voor kunnen nemen?
# change the wrong points
for x in range(0,len(listje)):
    
    
    left = listje[x][0]
    right = listje[x][1]
    print listdata6[int(left)-1][0]
    marge = abs(listdata6[int(left)-1][0]/2)
    #marge = 300
    print 'marge', marge
    co_left = listdata6[int(left)-1]
    print co_left
    co_right = listdata6[int(right)-1]
    print co_right
    distance_x = float(co_left[0]) + float(co_right[0])
    print 'distance', distance_x

    if distance_x > marge:
        if site == 0:
            listdata6[int(right)-1][0] = float(co_left[0]) * -1
            listdata6[int(right)-1][1] = float(co_left[1])
            listdata6[int(right)-1][2] = float(co_left[2])
        if site == 1:
            listdata6[int(left)-1][0] = float(co_right[0]) * -1
            listdata6[int(left)-1][1] = float(co_right[1])
            listdata6[int(left)-1][2] = float(co_right[2])
            
for x in range(0,len(listdata6)):
    output5.write("%.7f %.7f %.7f\n"%(listdata6[x][0], listdata6[x][1], listdata6[x][2]))

#print listdata
#print len(listdata)

datapoints.close()
mirrorpoints.close()


output.close()
output2.close()
output3.close()
output4.close()
output5.close()
