#Face creation part 1
#Rotate the object by points on symmetry axis
#Calculate points in faces and add them to ply file.

import math
from math import *
import sys
import numpy


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

########################################################################
file_outputname4 = 'outputrotate_faces.ply'
output4 = open(file_outputname4, 'w')

#name_file_ply = 'RMS_069_01_ascii.ply'
name_file_ply = raw_input('name ply file: ')
file_ply = open(name_file_ply)
#sympoints_file  = 'inputsym2.txt'
sympoints_file  = raw_input('name sym: ')
sympoints = open(sympoints_file)
symlines = sympoints.readlines()
listsym = []

name_file = name_file_ply
file1 = open(name_file)
var_col = 0
#ply file
for x in range(0, 20):
    readheader = file_ply.readline().strip().split()
    print readheader
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
        var_vertex_nm = readheader[2]

    if readheader[0] == "element" and readheader[1] == "face":
        var_face_ln = readheader[1]
        var_face_nm = readheader[2]

file_ply.close()        
listje = [] #sub list for coordinates
listtotal_vertex = [] #coordinates x,y,z list
listtotal_colors = []
sub_colors = []
print 'end header'
# symmetry points to list
for a  in range(0,len(symlines)):
    symline_1 = symlines[a].strip().split()
    listsym.append(symlines[a].strip().split())
    listtotal_vertex.append(symlines[a].strip().split())
   

for a in range(0, (int(var_header) + int(var_vertex_nm) + int(var_face_nm) + 1)):
    line = file1.readline().strip().split()
    if int(var_header) < a < (int(var_vertex_nm)+ int(var_header)+1):
        rayx = listje.append(line[0])
        rayy = listje.append(line[1])
        rayz = listje.append(line[2])
        listtotal_vertex.append(listje) #x y z coordinates to list
        listje = []
        if var_col != 0: #if color code is not 0
            color_x = sub_colors.append(line[3])
            color_y = sub_colors.append(line[4])
            color_z = sub_colors.append(line[5])
            listtotal_colors.append(sub_colors) #colors to list
            sub_colors = []
        
        

    
sym1 = listsym[0]
sym2 = listsym[1]
sym3 = listsym[2]
sym4 = listsym[3]
########### shifting object that sym3 point will be the zeropoint
print 'shifting object'
list2 = []
listdata3 = []
zeropoint = sym3

for c in range(0,len(listtotal_vertex)):
    list2.append(float(listtotal_vertex[c][0]) - float(zeropoint[0]))
    list2.append(float(listtotal_vertex[c][1]) - float(zeropoint[1]))
    list2.append(float(listtotal_vertex[c][2]) - float(zeropoint[2]))
    listdata3.append(list2)
    list2 = []


#########################
print 'rotate around z axis '
# Rotate around z axis #
# If object is upside down, 180 degrees rotation around the Z axis is needed.#
listdatatemp = []

sym_1 = listtotal_vertex[0]
sym_2 = listtotal_vertex[1]
sym_3 = listtotal_vertex[2]
sym_4 = listtotal_vertex[3]

if listdata3[0][1] < listdata3[2][1]:
    angle = 180
    for coordinates in range(0,len(listdata3)):
        listdatatemp.append(Z_rotation(listdata3[coordinates], angle))
    listdata3 = listdatatemp


# calculate angle rotation z
len_z_a = listdata3[0][0] - listdata3[2][0]

len_z_b = listdata3[0][1] - listdata3[2][1]
z_angle = (math.degrees(math.atan(len_z_a/len_z_b)))

# calculate new coordinates with rotation matrix of Z
listdata4 = []
for coordinates in range(0, len(listdata3)):
    listdata4.append(Z_rotation(listdata3[coordinates], z_angle))
listdata3 = []


print 'rotate around x axis '
# Rotate around x axis #
#calculate angle rotation x
len_x_a = listdata4[0][2] - listdata4[2][0]
len_x_b = listdata4[0][1] - listdata4[2][0]
x_angle = -(math.degrees(math.atan(len_x_a/len_x_b))) # waarom hier een min voor?

# calculate new coordinates with rotation matrix of X
listdata5 = []
for d in range(0, len(listdata4)):
    listdata5.append(X_rotation(listdata4[d], x_angle))
listdata4 = []


print 'rotate around y axis '
#Rotate around y axis#
#calculate angle rotation y
len_y_a = (listdata5[1][0] - listdata5[2][0])
len_y_b = (listdata5[1][2] - listdata5[2][2])
y_angle = -(math.degrees(math.atan(len_y_a/len_y_b)))

# calculate new coordinates with rotation matrix of Y
listdata6 = []
for d in range(0, len(listdata5)):
    listdata6.append(Y_rotation(listdata5[d], y_angle))

listdata5 = []
#Rotate 180 degrees around y axis when object is backwards.#
listdatatemp = []
if listdata6[1][0] < listdata6[3][0]: #point sym2_x < point sym 3
    angle = 180
    for coordinates in range(0,len(listdata6)):
        listdatatemp.append(Y_rotation(listdata6[coordinates], angle))
    listdata6 = listdatatemp

#writing new coordinates to outputfile, can be removed if program is correct
for x in range(0,len(listdata6)):
    output4.write("%.7f %.7f %.7f\n"%(listdata6[x][0], listdata6[x][1], listdata6[x][2]))


output4.close()

sympoints.close()
file_ply.close()
print 'newplyfile'
#writing new ply file with new points
file1.close()
outfile_rotating = open("outfile_rotating.ply", 'w') #create new file
pointsfile = open('outputrotate_faces.ply', 'r') #new points
file2= open(name_file_ply) #originele file

 
for d in range(0,(int(var_header) + int(var_vertex_nm) + int(var_face_nm) + 1)):
    line2 = file2.readline()
    readline2 = line2.strip().split()
    if d <= (int(var_header)): #header writing
        outfile_rotating.write('%s'%(line2))
    if d == int(var_header): #new coordinates writing
        line2 = file2.readline()
        readline2 = line2.strip().split()
        for f in range(0,len(listdata6)):
            line3 = pointsfile.readline()
            if f >= 4: #from point 4, because they were extra edit to the list in the beginning
                outfile_rotating.write('%s'%(line3))
                
    if d == (int(var_vertex_nm) + int(var_header)-1): #write the faces 
        for g in range(0, int(var_face_nm)):
            line2 = file2.readline()
            outfile_rotating.write('%s'%(line2))

        
outfile_rotating.close()
listdata6 = []
###############################################################################
# create new coordinates, middle of faces
name_file = 'outfile_rotating.ply'
file1 = open(name_file)
listje = []
listtotal_vertex = []
listtotal_face_sq = []
listtotal_face_tr = []
var_col = 0
outfile = open('sub_outfile_extra_coordinates.ply', 'w')


print 'find coordinates for each face'

# find coordinates for each face
for a in range(0, (int(var_header) + int(var_vertex_nm) + int(var_face_nm) + 1)):
    line = file1.readline().strip().split()
    if int(var_header) < a < (int(var_vertex_nm)+ int(var_header)+1):
        rayx = listje.append(line[0])
        rayy = listje.append(line[1])
        rayz = listje.append(line[2])
        listtotal_vertex.append(listje) #x y z coordinates to list
        listje = []
        
    if (int(var_vertex_nm)+ int(var_header)) < a < (int(var_vertex_nm) + int(var_header) + int(var_face_nm)+1):
        if int(line[0]) ==  4:
            listje.append(line[1])
            listje.append(line[2])
            listje.append(line[3])
            listje.append(line[4])
            listtotal_face_sq.append(listje) #square faces
            
            listje = []
        if int(line[0]) == 3:
            listje.append(line[1])
            listje.append(line[2])
            listje.append(line[3])
            listtotal_face_tr.append(listje) #triangle faces
            listje = []

#squares calculating
for b in range(0, len(listtotal_face_sq)):
    number1 = int(listtotal_face_sq[b][0])
    number2 = int(listtotal_face_sq[b][1])
    number3 = int(listtotal_face_sq[b][2])
    number4 = int(listtotal_face_sq[b][3])

    square1 = listtotal_vertex[number1]
    square2 = listtotal_vertex[number2]
    square3 = listtotal_vertex[number3]
    square4 = listtotal_vertex[number4]

    p1 = (float(square1[0]) + float(square2[0]) + float(square3[0]) + float(square4[0]))/4
    p2 = (float(square1[1]) + float(square2[1]) + float(square3[1]) + float(square4[1]))/4
    p3 = (float(square1[2]) + float(square2[2]) + float(square3[2]) + float(square4[2]))/4
    
    outfile.write("%.7f %.7f %.7f\n"%(p1,p2,p3)) #writing new points to file

newpoint = []
newpointtotal = []


# triangles calculating
for c in range(0, len(listtotal_face_tr)):
    number1 = int(listtotal_face_tr[c][0])
    number2 = int(listtotal_face_tr[c][1])
    number3 = int(listtotal_face_tr[c][2])
    triangle1 = listtotal_vertex[number1]
    triangle2 = listtotal_vertex[number2]
    triangle3 = listtotal_vertex[number3]
    
    p1 = (float(triangle1[0]) + float(triangle2[0]) + float(triangle3[0]))/3
    p2 = (float(triangle1[1]) + float(triangle2[1]) + float(triangle3[1]))/3
    p3 = (float(triangle1[2]) + float(triangle2[2]) + float(triangle3[2]))/3

    outfile.write("%.7f %.7f %.7f\n"%(p1,p2,p3)) #writing new points to file

outfile.close()

#writing new ply file with new points
file1.close()
outfile2 = open("outfile_new_points.ply", 'w')
pointsfile = open('sub_outfile_extra_coordinates.ply', 'r') #new points
file2= open(name_file) #originele file
g = 0

#for new coordinates, color code is 0,0,0     
for b in range(0, int(var_face_nm)):
    color_x = sub_colors.append('0')
    color_y = sub_colors.append('0')
    color_z = sub_colors.append('0')
    listtotal_colors.append(sub_colors) #colors to list
    sub_colors = []
    
for d in range(0,(int(var_header) + int(var_vertex_nm) + int(var_face_nm) + 1)):
    line2 = file2.readline().strip()
    readline2 = line2.strip().split()
    if readline2[0] == "element" and readline2[1] == "vertex":
        outfile2.write("element vertex %s\n"%(int(var_vertex_nm) + int(var_face_nm))) #number of vertexen changing
    
    elif (int(var_header) < d < (int(var_header) + int(var_vertex_nm))): #rotated vertexen, with original color code
        outfile2.write('%s %s %s %s\n'%(line2, listtotal_colors[g][0], listtotal_colors[g][1], listtotal_colors[g][2]))
        g += 1
        
    elif (int(var_header) + int(var_vertex_nm)) == d: #for new vertexen, with color code 0,0,0
        outfile2.write('%s %s %s %s\n'%(line2,listtotal_colors[g][0], listtotal_colors[g][1], listtotal_colors[g][2])) #the last original vertex
        g += 1
        

        for x in range(0, int(var_face_nm)): # the new vertexen, with color code
            line3 = pointsfile.readline().strip()
            outfile2.write('%s %s %s %s\n'%(line3, listtotal_colors[g][0], listtotal_colors[g][1], listtotal_colors[g][2]))
            g += 1
        
    else: #everything left
        outfile2.write('%s\n'%(line2))
        
      
outfile2.close()
print 'it worked'
###################################################################################################################

