# Rotate ply file to normalized position
# based at points on symmetry axis
# MB

import math
from math import *
import sys
import numpy

# Main function
def main():
    # input user .ply file
    name_file_ply = sys.argv[1]
    # input user symmetry points file
    sym_points_file  = sys.argv[2]

    # to function 'extracting header', return header features
    var_header,var_vertex_nm,var_face_nm, var_col = extracting_header(name_file_ply)

    # to function 'extracting symmetry points', return symmetry points and list with new vertex
    listsym,listtotal_vertex = extracting_symmetry_points(sym_points_file)

    # to function 'extracting coordiantes', return list vertex and colors
    listtotal_vertex, listtotal_colors = extracting_coordinates(name_file_ply,
                                                                var_header,var_vertex_nm,var_face_nm,
                                                                listtotal_vertex, var_col)
    # to function 'shift to zero'
    shift_to_zero(listsym,listtotal_vertex)

    # to function 'write ply file'
    write_ply_file(name_file_ply, var_header,var_vertex_nm,var_face_nm,
                   listtotal_colors, listtotal_vertex)

    
# Function to extract all the values of the header of the ply file
def extracting_header(name_file_ply):
    file_ply = open(name_file_ply) # open ply file
    var_col = 0 # color variable
    count = 0 # counter 

    # for the first lines of the ply file
    for line in range(0, 40):
        readheader = file_ply.readline().strip().split()
        if len(readheader) != 0:
            if readheader[0] == 'end_header':
                var_header = count
                
            # If there are colors in the ply file    
            if 'red' in readheader:
                var_col += 1
            if 'blue' in readheader:
                var_col += 1
            if 'green' in readheader:
                var_col += 1
                
            # extracting number of vertexen    
            if readheader[0] == "element" and readheader[1] == "vertex":
                var_vertex_nm = readheader[2]
                
            # extracting number of faces    
            if readheader[0] == "element" and readheader[1] == "face":
                var_face_nm = readheader[2]
            count += 1
        else:
            continue
    
    file_ply.close() # closing ply file
    return var_header, var_vertex_nm,var_face_nm, var_col    # return values to main

# Function for extracting the values of the symmetry points file
def extracting_symmetry_points(sym_points_file):
    sympoints = open(sym_points_file) # open symmetry file
    symlines = sympoints.readlines() # read all the lines of file
    listsym = [] # symmetry points
    listtotal_vertex = [] # vertexen
    # every line in the sym file
    for sym in range(0,len(symlines)):
        symline_1 = symlines[sym].strip().split()
        listsym.append(symlines[sym].strip().split()) #add symmetry points  
        listtotal_vertex.append(symlines[sym].strip().split()) # add symmetry points

    sympoints.close() # close symmetry file
    return listsym,listtotal_vertex # return symmetry points list and vertex list 
    
                           
# Function to extract the coordinates of the ply file
def extracting_coordinates(name_file_ply, var_header,var_vertex_nm,var_face_nm, listtotal_vertex, var_col):
    file1 = open(name_file_ply) # open ply file

    sub_list = [] #sublist coordinates
    listtotal_colors = [] # color list
    sub_colors = [] # sublist color

    # coordinates of ply file to list
    for coordinates_ln in range(0, (int(var_header) + int(var_vertex_nm) + int(var_face_nm) + 1)):
        line = file1.readline().strip().split()
        if (int(var_header) < coordinates_ln < (int(var_vertex_nm)+ int(var_header)+1)):
            rayx = sub_list.append(line[0])
            rayy = sub_list.append(line[1])
            rayz = sub_list.append(line[2])
            listtotal_vertex.append(sub_list) #x y z coordinates to list
            sub_list = []
            if var_col != 0: #if color code is not 0
                color_x = sub_colors.append(line[3])
                color_y = sub_colors.append(line[4])
                color_z = sub_colors.append(line[5])
                listtotal_colors.append(sub_colors) #colors to list
                sub_colors = []
        
    return listtotal_vertex, listtotal_colors # return coordinates (vertexen) and color lists


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

#Function to shift the object to the zeropoint
def shift_to_zero(listsym, listtotal_vertex):
    sym3 = listsym[2]
    zeropoint = sym3
    list2 = [] # sublist coordinates
    listdata3 = [] # new coordinates
    # every coordinate minus the sym3 coordinates 
    for vertex in range(0,len(listtotal_vertex)):
        list2.append(float(listtotal_vertex[vertex][0]) - float(zeropoint[0]))
        list2.append(float(listtotal_vertex[vertex][1]) - float(zeropoint[1]))
        list2.append(float(listtotal_vertex[vertex][2]) - float(zeropoint[2]))
        listdata3.append(list2) # add new coordinates to list
        list2 = []

    # to function 'rotate z axis'
    rotate_z_axis(listdata3)

# Function for rotating the object around z axis
def rotate_z_axis(listdata3):
    # If object is upside down, 180 degrees rotation around the Z axis is needed.
    listdatatemp = []
    # check if object is upside down
    if listdata3[0][1] < listdata3[2][1]:
        angle = 180
        # rotate 180 degrees. 
        for coordinates in range(0,len(listdata3)):
            listdatatemp.append(Z_rotation(listdata3[coordinates], angle))
        listdata3 = listdatatemp # new coordinates


    # calculate angle rotation z
    len_z_a = listdata3[0][0] - listdata3[2][0]
    len_z_b = listdata3[0][1] - listdata3[2][1]
    z_angle = (math.degrees(math.atan(len_z_a/len_z_b)))

    # calculate new coordinates with rotation matrix of Z
    listdata4 = []
    for coordinates in range(0, len(listdata3)):
        listdata4.append(Z_rotation(listdata3[coordinates], z_angle)) # add new coordinates to list
    listdata3 = []
    
    # to function 'rotate x axis'
    rotate_x_axis(listdata4)

# Function for rotating the object around x axis
def rotate_x_axis(listdata4):
    #calculate angle rotation x
    len_x_a = listdata4[0][2] - listdata4[2][0]
    len_x_b = listdata4[0][1] - listdata4[2][0]
    x_angle = -(math.degrees(math.atan(len_x_a/len_x_b)))

    # calculate new coordinates with rotation matrix of X
    listdata5 = []
    for coordinates in range(0, len(listdata4)):
        listdata5.append(X_rotation(listdata4[coordinates], x_angle)) # add new coordinates to list
    listdata4 = []

    # to function 'rotate y axis'
    rotate_y_axis(listdata5)

# Function for rotating the object around y axis
def rotate_y_axis(listdata5):
    #calculate angle rotation y
    len_y_a = (listdata5[1][0] - listdata5[2][0])
    len_y_b = (listdata5[1][2] - listdata5[2][2])
    y_angle = -(math.degrees(math.atan(len_y_a/len_y_b)))

    # calculate new coordinates with rotation matrix of Y
    listdata6 = []
    for coordinates in range(0, len(listdata5)):
        listdata6.append(Y_rotation(listdata5[coordinates], y_angle))

    listdata5 = []
    #Rotate 180 degrees around y axis when object is backwards.#
    listdatatemp = []
    if listdata6[1][0] < listdata6[3][0]: #point sym2_x < point sym 3
        angle = 180
        for coordinates in range(0,len(listdata6)):
            listdatatemp.append(Y_rotation(listdata6[coordinates], angle)) # add new coordinates to list
        listdata6 = listdatatemp

    # to function 'write new coordinates'
    write_new_coordinates(listdata6)

# Function write the new coordinates to outputfile. 
def write_new_coordinates(listdata6):
    file_outputname4 = 'outputrotate_points.ply' # sub outputfile
    output4 = open(file_outputname4, 'w')

    # write every coordinate to output file
    for line in range(0,len(listdata6)):
        output4.write("%.7f %.7f %.7f\n"%(listdata6[line][0], listdata6[line][1], listdata6[line][2]))

# Function to write the new ply file with 
def write_ply_file(name_file_ply, var_header,var_vertex_nm,var_face_nm, listtotal_colors, listtotal_vertex):
    outfile_rotating2 = open(sys.argv[3], 'w') #create new file
    pointsfile = open('outputrotate_points.ply', 'r') #new points
    file2= open(name_file_ply) #original ply file
    counter = 0 # counter for color

    # writing all the parts of the new ply file
    for line in range(0,(int(var_header) + int(var_vertex_nm) + int(var_face_nm) + 1)):
        line2 = file2.readline()
        readline2 = line2.strip().split()
        if line <= (int(var_header)): #header writing
            outfile_rotating2.write('%s'%(line2))
        if line == int(var_header): #new coordinates writing
            line2 = file2.readline()
            readline2 = line2.strip().split()
            for vertex in range(0,len(listtotal_vertex)):
                line3 = pointsfile.readline().strip()
                if vertex >= 4: #from point 4, because they were extra edit to the list in the beginning
                    outfile_rotating2.write('%s %s %s %s\n'%
                                            (line3, listtotal_colors[counter][0],
                                             listtotal_colors[counter][1], listtotal_colors[counter][2]))
                    counter += 1
        if line == (int(var_vertex_nm) + int(var_header)-1): #write the faces 
            for face in range(0, int(var_face_nm)):  
                line2 = file2.readline()
                outfile_rotating2.write('%s'%(line2))
    counter = 0        

    outfile_rotating2.close() # outputfile close

main()
