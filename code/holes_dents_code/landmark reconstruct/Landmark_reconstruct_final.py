#Program for correcting landmarks.
#The object will be rotated, based on 3 symmetry points.
#The differences between the mirror points will be calculated and the coordinates will be corrected where needed.



import math
from math import *
import sys
import numpy
import os

#file_name = raw_input("file dta: ") #dta file
file_name = sys.argv[1] #dta file
#file_name = 'RMS70_1.dta'
#file_connect = raw_input("file connect landmarks: ")
file_connect = sys.argv[2]
#file_connect= 'mirror3.txt' # connecter file

#output files
file_outputname = 'outputrotate.dta'
file_outputname2 = 'outputrotate2.dta'
file_outputname3 = 'outputrotate3.dta'
#file_outputname4 = 'outputrotate4.dta'
#file_outputname5 = 'outputcorrected.dta'
file_outputname4 = sys.argv[4]
file_outputname5 = sys.argv[5]

#open output files
output = open(file_outputname, 'w')
output2 = open(file_outputname2, 'w')
output3 = open(file_outputname3, 'w')
output4 = open(file_outputname4, 'w')
output5 = open(file_outputname5, 'w')

# User input if left or right site is good.
site = sys.argv[3]

site = int(site)
datapoints = open(file_name)
datalines = datapoints.readlines()
listdata = []
listdta = []
sublistje = []

# open dta file
for a  in range(0,len(datalines)):
    aline = datalines[a].strip()
    listdta.append(datalines[a].strip().split('  '))

    #numbers in dta file to list
    if len(listdta[a]) == 3:
        sublistje.append(float(listdta[a][0]))
        sublistje.append(float(listdta[a][1]))
        sublistje.append(float(listdta[a][2]))
        listdata.append(sublistje)
        sublistje = []
        
    #write header of dta file to outputfile
    else:
        output.write("%s\n"%(aline))
	output5.write("%s\n"%(aline))

# open mirrorpoints file
mirrorpoints = open(file_connect)
lines= mirrorpoints.readlines()
listje = [] #with mirror points
listjesym = [] #with symmetry points
listspec = []

#extracting symmetry landmarks and mirror landmarks of connect file
for x in range(0, len(lines)):
    line = lines[x].strip()
    if line == 'sym':
        for a in range(1,4):
            listjesym.append(lines[a].strip().split())
    if line == 'mirror':
        for y in range(x + 1,len(lines)):
            try:
                if lines[y].strip() != 'spec':
                    if lines[y].strip() == '':
                        break
                    else:
                        listje.append(lines[y].strip().split())
                    
                else:
                    break
                    #listje.append(lines[y].strip().split())
            except:
                break
    if line == 'spec':
        for b in range(x+1, len(lines)):
            listspec.append(lines[b].strip().split())


#Symmetry points
sym1 = int(listjesym[0][0]) -1
sym2 = int(listjesym[1][0]) -1 
sym3 = int(listjesym[2][0]) -1


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


# shifting object that sym3 point will be the zeropoint #
zeropoint = int(sym3)

co_zeropoint = listdata[zeropoint] #coordinates of sym3

listdata2 = []
listdata3 = []

# minus x,y,z of point shift to zeropoint of every point
for x in range(0,len(listdata)):
    listdata2.append(listdata[x][0] - co_zeropoint[0])
    listdata2.append(listdata[x][1] - co_zeropoint[1])
    listdata2.append(listdata[x][2] - co_zeropoint[2])
    listdata3.append(listdata2)
    listdata2 = []

#writing new coordinates to outputfile, can be removed if program is correct
for x in range(0,len(listdata)):
    output.write("%s %s %s\n"%(listdata3[x][0], listdata3[x][1], listdata3[x][2]))
output.close()



# Rotate around z axis #
# If object is upside down, 180 degrees rotation around the Z axis is needed.#
listdatatemp = []

if listdata3[sym1][1] < listdata3[sym3][1]:
    angle = 180
    for coordinates in range(0,len(listdata3)):
        listdatatemp.append(Z_rotation(listdata3[coordinates], angle))
    listdata3 = listdatatemp


# calculate angle rotation z
len_z_a = listdata3[int(sym1)][0] - listdata3[int(sym3)][0]
len_z_b = listdata3[int(sym1)][1] - listdata3[int(sym3)][1]
z_angle = (math.degrees(math.atan(len_z_a/len_z_b)))

# calculate new coordinates with rotation matrix of Z
listdata4 = []
for coordinates in range(0, len(listdata3)):
    listdata4.append(Z_rotation(listdata3[coordinates], z_angle))

#writing new coordinates to outputfile, can be removed if program is correct
for x in range(0,len(listdata)):
    output2.write("%.7f %.7f %.7f\n"%(listdata4[x][0], listdata4[x][1], listdata4[x][2]))



# Rotate around x axis #
#calculate angle rotation x
len_x_a = listdata4[int(sym1)][2] - listdata4[int(sym3)][0]
len_x_b = listdata4[int(sym1)][1] - listdata4[int(sym3)][0]
x_angle = -(math.degrees(math.atan(len_x_a/len_x_b))) # waarom hier een min voor?

# calculate new coordinates with rotation matrix of X
listdata5 = []
for d in range(0, len(listdata3)):
    listdata5.append(X_rotation(listdata4[d], x_angle))

#writing new coordinates to outputfile, can be removed if program is correct
for x in range(0,len(listdata)):
    output3.write("%.7f %.7f %.7f\n"%(listdata5[x][0], listdata5[x][1], listdata5[x][2]))



#Rotate around y axis#
#calculate angle rotation y
len_y_a = (listdata5[int(sym2)][0] - listdata5[int(sym3)][0])
len_y_b = (listdata5[int(sym2)][2] - listdata5[int(sym3)][2])
y_angle = -(math.degrees(math.atan(len_y_a/len_y_b)))

# calculate new coordinates with rotation matrix of Y
listdata6 = []
for d in range(0, len(listdata5)):
    listdata6.append(Y_rotation(listdata5[d], y_angle))


#Rotate 180 degrees around y axis when object is backwards.#
listdatatemp = []
if listdata6[sym2][0] < listdata6[(int(listje[0][0]))][0]: #point sym2_x < point mirror 1_x
    angle = 180
    for coordinates in range(0,len(listdata6)):
        listdatatemp.append(Y_rotation(listdata6[coordinates], angle))
    listdata6 = listdatatemp

#writing new coordinates to outputfile, can be removed if program is correct
for x in range(0,len(listdata5)):
    output4.write("%.7f %.7f %.7f\n"%(listdata6[x][0], listdata6[x][1], listdata6[x][2]))


  
#Correcting landmarks#
percentage_distance = []
if len(listspec) == 0:
        
    #calculate marge of distance
    for x in range(0,len(listje)):  
        left = listje[x][0] #left landmark
        right = listje[x][1] #right landmark
        co_left = listdata6[int(left)-1] #left landmark coordinates
        co_left_x = co_left[0] # left landmark coordinate x
        co_right = listdata6[int(right)-1]#right landmark coordinates
        co_right_x = co_right[0] #right landmark coordinate x
        distance_x = float(co_left[0]) + float(co_right[0])
        
        # if left is correct
        if site == 0:
            percentage_distance.append(abs(distance_x) / abs(co_left_x)) #percentage 

        # if right is correct
        elif site == 1:
            percentage_distance.append(abs(distance_x) / abs(co_right_x)) #percentage
        else:
            print 'something wrong'


    mean_percentage = numpy.mean(percentage_distance) #mean of percentages
    std_percentage = numpy.std(percentage_distance)
    #range of correct values


    #t = (mean_percentage * 34.1) / 100 #68.2 is one standard deviation
    left_range = mean_percentage - std_percentage #left range mean minus one standard deviation
    right_range = mean_percentage + std_percentage # rigth range mean plus one standard deviation

    #correcting the landmarks coordinates#
    for x in range(0,len(listje)):
        left = listje[x][0]
        right = listje[x][1]
        co_left = listdata6[int(left)-1]
        co_right = listdata6[int(right)-1]
        #if there is to much deviation take correct coordinate and project it to the other side. 
        if (percentage_distance[x] > right_range) or (percentage_distance[x] < left_range):
            
            #if left side is correct
            if site == 0:
                listdata6[int(right)-1][0] = float(co_left[0]) * -1
                listdata6[int(right)-1][1] = float(co_left[1])
                listdata6[int(right)-1][2] = float(co_left[2])
            #if right side is correct 
            if site == 1:
                listdata6[int(left)-1][0] = float(co_right[0]) * -1
                listdata6[int(left)-1][1] = float(co_right[1])
                listdata6[int(left)-1][2] = float(co_right[2])


# if there are points in spec, the wrong points will be replaced with the coordinates of the opposite landmark    
else:
    for x in range(0,len(listspec)):
        number = listspec[x][0]
        for spec in range(0, len(listje)):
            try: 
                pos = listje[spec].index(number) #find number in mirror list
                #extracting the opposite landmark number
                if pos == 0: 
                    number2 = listje[spec][1]
                elif pos == 1 :
                    number2 = listje[spec][0]
                else:
                    print 'fout'
                #replace the wrong coordinates 
                listdata6[int(number)-1][0] = float(listdata6[int(number2)-1][0])*-1
                listdata6[int(number)-1][1] = float(listdata6[int(number2)-1][1])
                listdata6[int(number)-1][2] = float(listdata6[int(number2)-1][2])  
            except:
                continue

# write corrected coordinates to file.          
for x in range(0,len(listdata6)):
    output5.write("%.7f  %.7f  %.7f\n"%(listdata6[x][0], listdata6[x][1], listdata6[x][2]))

#close all files
datapoints.close()
mirrorpoints.close()
output.close()
output2.close()
output3.close()
output4.close()
output5.close()
