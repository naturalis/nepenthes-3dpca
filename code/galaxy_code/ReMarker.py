#Program for correcting landmarks.
#The object will be rotated, based on 3 symmetry points.
#The differences between the mirror points will be calculated and
# the coordinates will be corrected where needed.

#MB

import math
from math import *
import sys
import numpy
import os

# Main function
def main():
    file_name = sys.argv[1] # dta file
    file_connect = sys.argv[2] # connect file
    side = sys.argv[3] # correct side of object
    
    file_outputname5 = sys.argv[5] # output dta file
    output5 = open(file_outputname5, 'w')

    # to function 'open connect file'
    sym1,sym2,sym3, listmirror, listspec = open_connect_file(file_connect)

    # to function 'open dta file'
    listdata = open_dta_file(file_name, output5)

    # to function 'shift to zero'
    shift_to_zero(listdata,sym1,sym2,sym3,listmirror,listspec, side, output5)
    
# Function for extracting values of connect file
def open_connect_file(file_connect):
    mirrorpoints = open(file_connect)
    lines= mirrorpoints.readlines()
    listmirror = [] #with mirror points
    listsym = [] #with symmetry points
    listspec = [] #with spec points

    #extracting symmetry landmarks and mirror landmarks of connect file
    for x in range(0, len(lines)):
        line = lines[x].strip()
        if line == 'sym': # extract points on symmetry plane
            for a in range(1,4):
                listsym.append(lines[a].strip().split())
        if line == 'mirror': #  extract mirror points
            for y in range(x + 1,len(lines)):
                try:
                    if lines[y].strip() != 'spec':
                        if lines[y].strip() == '':
                            break
                        else:
                            listmirror.append(lines[y].strip().split()) # add mirror points 
                        
                    else:
                        break
                        
                except:
                    break
        if line == 'spec':# if specs are present
            for b in range(x+1, len(lines)):
                listspec.append(lines[b].strip().split()) # add points in specs
    #Symmetry points
    sym1 = int(listsym[0][0]) -1
    sym2 = int(listsym[1][0]) -1 
    sym3 = int(listsym[2][0]) -1
    
    mirrorpoints.close()
    return sym1, sym2, sym3, listmirror, listspec

# Function open .dta file
def open_dta_file(file_name, output5):
    datapoints = open(file_name)#open file
    datalines = datapoints.readlines()
    listdata = [] # landmarklist
    listdta = [] # coordinates
    sublist = [] # sublist
    for a  in range(0,len(datalines)):
        aline = datalines[a].strip()
        listdta.append(datalines[a].strip().split('  ')) # notice space

        #numbers in dta file to list
        if len(listdta[a]) == 3:
            sublist.append(float(listdta[a][0]))
            sublist.append(float(listdta[a][1]))
            sublist.append(float(listdta[a][2]))
            listdata.append(sublist)
            sublist = []
            
        #write header of dta file to outputfile
        else:
            output5.write("%s\n"%(aline))

    datapoints.close()
    return listdata

# Function to calculate the values in the Z rotation matrix
def Rz_matrix(z_angle): # Rz rotation matrix
    return [[cos(math.radians(z_angle)), -sin(math.radians(z_angle)), 0.0],[sin(math.radians(z_angle)),cos(math.radians(z_angle)),0.0],[0.0, 0.0, 1.0]]

# Function to calculate the new coordinates rotated with Z rotation matrix
def Z_rotation(point2, z_angle): # multiplication rotation matrix and coordinates 
    r_z = Rz_matrix(z_angle)
    rotated_z = []               
    for i in range(3):
        rotated_z.append((sum([r_z[i][j] * point2[j] for j in range(3)])))
    return rotated_z

# Function to calculate the values in the X rotation matrix
def Rx_matrix(x_angle): #rotation matrix x-axis
    return [[1, 0, 0],[0,cos(math.radians(x_angle)),-sin(math.radians(x_angle))],[0,sin(math.radians(x_angle)),cos(math.radians(x_angle))]]

# Function to calculate the new coordinates rotated with X rotation matrix
def X_rotation(point3, x_angle): #multiplication rotation matrix and coordinates 
    r_x = Rx_matrix(x_angle)
    rotated_x = []  
    for i in range(3):
        rotated_x.append((sum([r_x[i][j] * point3[j] for j in range(3)])))
    return rotated_x

# Function to calculate the values in the Y rotation matrix
def Ry_matrix(y_angle): # Ry rotation matrix
    return [[cos(math.radians(y_angle)), 0.0, sin(math.radians(y_angle))],[0.0, 1.0, 0.0],[-sin(math.radians(y_angle)),0.0, cos(math.radians(y_angle))]]

# Function to calculate the new coordinates rotated with Y rotation matrix
def Y_rotation(point4, y_angle): #multiplication rotation matrix and coordinates 
    r_y = Ry_matrix(y_angle)
    rotated_y = []
    for i in range(3):
        rotated_y.append((sum([r_y[i][j] * point4[j] for j in range(3)])))
    return rotated_y 

# Function shift object to zeropoint
def shift_to_zero(listdata, sym1,sym2,sym3, listmirror, listspec, side,output5):
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
    rotate_z_axis(listdata3,sym1,sym2,sym3, listmirror, listspec, side, output5)


# Function for rotating the object around z axis
def rotate_z_axis(listdata3, sym1,sym2,sym3, listmirror, listspec, side, output5):
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

    rotate_x_axis(listdata4,sym1,sym2,sym3, listmirror, listspec, side, output5)

# Function for rotating the object around x axis  
def rotate_x_axis(listdata4,sym1,sym2,sym3, listmirror, listspec, side, output5):
    #calculate angle rotation x
    len_x_a = listdata4[int(sym1)][2] - listdata4[int(sym3)][0]
    len_x_b = listdata4[int(sym1)][1] - listdata4[int(sym3)][0]
    x_angle = -(math.degrees(math.atan(len_x_a/len_x_b))) 

    # calculate new coordinates with rotation matrix of X
    listdata5 = []
    for d in range(0, len(listdata4)):
        listdata5.append(X_rotation(listdata4[d], x_angle))

    rotate_y_axis(listdata5,sym1,sym2,sym3, listmirror, listspec, side, output5)

# Function for rotating the object around y axis    
def rotate_y_axis(listdata5,sym1,sym2,sym3,listmirror, listspec, side, output5):
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
    if listdata6[sym2][0] < listdata6[(int(listmirror[0][0]))][0]: #point sym2_x < point mirror 1_x
        angle = 180
        for coordinates in range(0,len(listdata6)):
            listdatatemp.append(Y_rotation(listdata6[coordinates], angle))
        listdata6 = listdatatemp
    write_rotate_co(listdata6)

    # to correcting the landmarks
    if len(listspec) == 0:
        correct_landmarks(listdata6, listmirror, side, output5)
    else:
        correct_specs(listdata6, listmirror, listspec, output5)        

# Function writing rotated coordinates to file
def write_rotate_co(listdata6):
    file_outputname4 = sys.argv[4]
    output4 = open(file_outputname4, 'w')
    #writing new coordinates to outputfile
    for x in range(0,len(listdata6)):
        output4.write("%.7f\t%.7f\t%.7f\n"%(listdata6[x][0], listdata6[x][1], listdata6[x][2]))

#Function for correcting the landmarks     
def correct_landmarks(listdata6, listmirror, side,output5):

    percentage_distance = []
    #calculate marge of distance
    for x in range(0,len(listmirror)):  
        left = listmirror[x][0] #left landmark
        right = listmirror[x][1] #right landmark
        co_left = listdata6[int(left)-1] #left landmark coordinates
        co_left_x = co_left[0] # left landmark coordinate x
        co_right = listdata6[int(right)-1]#right landmark coordinates
        co_right_x = co_right[0] #right landmark coordinate x
        distance_x = float(co_left[0]) + float(co_right[0])
        
        # if left is correct
        if int(side) == 0:
            percentage_distance.append(abs(distance_x) / abs(co_left_x)) #percentage 

        # if right is correct
        elif int(side) == 1:
            percentage_distance.append(abs(distance_x) / abs(co_right_x)) #percentage
        else:
            print 'something wrong'


    mean_percentage = numpy.mean(percentage_distance) #mean of percentages
    std_percentage = numpy.std(percentage_distance)
    #range of correct values
    left_range = mean_percentage - std_percentage #left range mean minus one standard deviation
    right_range = mean_percentage + std_percentage # rigth range mean plus one standard deviation

    #correcting the landmarks coordinates#
    for x in range(0,len(listmirror)):
        left = listmirror[x][0]
        right = listmirror[x][1]
        co_left = listdata6[int(left)-1]
        co_right = listdata6[int(right)-1]
        #if there is to much deviation take correct coordinate and project it to the other side. 
        if (percentage_distance[x] > right_range) or (percentage_distance[x] < left_range):
            
            #if left side is correct
            if int(side) == 0:
                listdata6[int(right)-1][0] = float(co_left[0]) * -1
                listdata6[int(right)-1][1] = float(co_left[1])
                listdata6[int(right)-1][2] = float(co_left[2])
            #if right side is correct 
            if int(side) == 1:
                listdata6[int(left)-1][0] = float(co_right[0]) * -1
                listdata6[int(left)-1][1] = float(co_right[1])
                listdata6[int(left)-1][2] = float(co_right[2])
    write_output(listdata6,output5)

#Function for correcting landmarks, defined in specs
def correct_specs(listdata6, listmirror, listspec,output5):
    for x in range(0,len(listspec)):
        number = listspec[x][0]
        for spec in range(0, len(listmirror)):
            try: 
                pos = listmirror[spec].index(number) #find number in mirror list
                #extracting the opposite landmark number
                if pos == 0: 
                    number2 = listmirror[spec][1]
                elif pos == 1 :
                    number2 = listmirror[spec][0]
                else:
                    print 'wrong'
                #replace the wrong coordinates 
                listdata6[int(number)-1][0] = float(listdata6[int(number2)-1][0])*-1
                listdata6[int(number)-1][1] = float(listdata6[int(number2)-1][1])
                listdata6[int(number)-1][2] = float(listdata6[int(number2)-1][2])  
            except:
                continue
    write_output(listdata6,output5)

#Function for writing the corrected landmarks to outputfile
def write_output(listdata6,output5):

    for x in range(0,len(listdata6)):
        output5.write("%.7f  %.7f  %.7f\n"%(listdata6[x][0], listdata6[x][1], listdata6[x][2]))
    output5.close()
main()
