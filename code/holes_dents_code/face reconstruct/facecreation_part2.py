#second part of face creation program
#places the points in boxes so you can compare the boxes with eachother?

import math
from math import *
import sys
import numpy

name_file_ply = 'outfile_rotating2.ply'
output = open('new_coordinates.ply', 'w')
file_ply = open(name_file_ply)
var_col = 0
site = 1 #MOET NOG VERANDERD WORDEN
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
rangenm = float(var_vertex_nm)/ 100000 #moet die 100000 zijn?
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


print number_of_boxes_ver, 'number_of_boxes_ver'
print number_of_boxes_hor, 'number_of_boxes_hor'
lijst_range = []
dictiolijst_co = {} #dictionary
x_start1 = 0.0
x_start2 = 0.0
x_window_max1 = 0.0
x_window_max2 = 0.0
y_window_min = lowest_y
y_window_max = lowest_y

print 'creating the dictionary'
#creating the dictionary with the varname as key and a empty list as value
for a in range(0,int(number_of_boxes_ver)): #number of rows
    for b in range(0, int((2*number_of_boxes_hor))): #number of columns
        varname = "%s_%s"%(a,b)
        dictiolijst_co[varname] = []
print len(dictiolijst_co)
print 'filling the list'
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

print 'filling the coordinates in the box'
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
                
#print dictiolijst_co
################################ new part for mean
newdictio = {}
x = 0
total  = 0
gemiddeldetotaal = 0
print 'calculate mean'
for x in range(0,int(number_of_boxes_ver)):
    for y in range(0, int((2*number_of_boxes_hor))):
        varname = "%s_%s"%(x,y)
        #print varname
        d = dictiolijst_co.get(varname)
        #print d
        try:
            if len(d) == 0:
                newdictio[varname] = 0 #dit klopt niet
            else: 
                for e in range(0,len(d)):
                    total += float(d[e][0])
                gemiddelde  = total/(len(d))
                #gemiddeldetotaal += gemiddelde
                newdictio[varname] = gemiddelde
                total = 0
        except:
            continue


counter = 0
difference = 0
lijstje2 = []
print 'calculating mean and stdev'
#for calculating mean and stdev.
for x in range(0, int(2*number_of_boxes_hor)):
    y = 0 
    while True:
        if y < int(number_of_boxes_ver):
            varname1 = "%s_%s"%(x,y)
            varname2 = "%s_%s"%(x,y+1)
            d = newdictio.get(varname1)
            f = newdictio.get(varname2)
            try:
                lijstje2.append(abs(d-f))
                counter += 1
            except:
                y += 2
                continue
            y += 2
        else:
            break

#print 'lijstje2', lijstje2
counter = 0
mean_percentage = numpy.mean(lijstje2) #gemiddelde van de verschillen tussen de vakjes
print mean_percentage, 'mean percentage'
std_percentage = numpy.std(lijstje2) # standard deviatie der van
print std_percentage, 'std'

left_range = mean_percentage - std_percentage #left range mean minus one standard deviation
right_range = mean_percentage + std_percentage

#######
#left_range = 2.20
#print left_range ,'left_range'
#print right_range, 'right_range'
co = []
lijstje2 = []
print 'calculating differences in range'
#for calculating if difference in range 
for x in range(0, int(2*number_of_boxes_hor)):
    y = 0 
    while True:
        if y < int(number_of_boxes_ver):
            varname1 = "%s_%s"%(x,y)
            varname2 = "%s_%s"%(x,y+1)
            d = newdictio.get(varname1)
            f = newdictio.get(varname2)
            #print varname1, 'varname'
            try:
                difference = abs(float(d)-float(f))
                #print 'difference', difference
                if (difference > right_range) or (difference < left_range):
                    if site == 0:
                        b = (dictiolijst_co.get(varname2))
                        for i in range (0, len(b)):
                            co.append(b[i])
                    elif site == 1:
                        b = (dictiolijst_co.get(varname1))
                        for i in range (0, len(b)):
                            co.append(b[i])
                counter += 1
            except:
                y += 2
                continue
            y += 2
        else:
            break
#print co
print 'write newcoordinates with colorcode to ouputfile'
output.write("ply\nformat ascii 1.0\ncomment Createdddddd By NextEngine ScanStudio\n")
output.write("element vertex %s\n"%(len(co)))
output.write("property float x\nproperty float y\nproperty float z\nproperty uchar red\nproperty uchar green\nproperty uchar blue\n")
output.write("element face %s\n"%(len(co)))
output.write("property list uchar int vertex_indices\nend_header\n")
#writing the newcoordinates with colorcode to ouputfile
for a in range(0,len(co)):
    getal = float(co[a][0])
    co[a][0] = (getal * -1)
    
    #print co[a][0]
    output.write('%s %s %s 230 0 182 \n'%(co[a][0], float(co[a][1]), float(co[a][2])))



      
file1.close()
file1 = open(name_file_ply)
C = []
sub = []
print 'calculating the nearest 2 points'
#calculating the nearest 2 points of point of interest 
for b in range(0, len(co)):
    closestDist1 = 1000000000
    closestDist2 = 1000000000
    count= 0
    for c in range(0,len(co)):
        dist1 = ((float(co[b][0])- float(co[c][0]))**2) +((float(co[b][1])-float(co[c][1]))**2) +((float(co[b][2])-float(co[c][2]))**2) #klopt dit?
        dist2 = ((float(co[b][0])- float(co[c][0]))**2) +((float(co[b][1])-float(co[c][1]))**2) +((float(co[b][2])-float(co[c][2]))**2)#klopt dit?
        if count < 1: 
            first = (co[b])
            second = co[c]
            third = co[c]
            count = 1
        if closestDist1 > dist1 and dist1 != 0:
            if third == first:
                third = second
            second = co[c]

            closestDist1 = dist1
            
                
        elif closestDist2 > dist2 and dist2 != 0:
            third = co[c]
            closestDist2 = dist2

        else:
            continue

    sub.append(co[b])
    sub.append(second)
    sub.append(third)
    C.append(sub)
    sub = []
outfile2 = open('new_plyfile.ply', 'w')
#print C
g = 0

print len(C)
print len(co)
for d in range(0,(int(var_header) + int(var_vertex_nm) + int(var_face_nm) + 1)):
    line2 = file1.readline().strip()
    readline2 = line2.strip().split()
    if readline2[0] == "element" and readline2[1] == "vertex":
        outfile2.write("element vertex %s\n"%(int(var_vertex_nm) + int(len(co)))) #number of vertexen changing
                       
    elif readline2[0] == "element" and readline2[1] == "face":
        outfile2.write("element face %s\n"%(int(var_face_nm) + int(len(C)))) #number of vertexen changing                                      
    elif (int(var_header) < d < (int(var_header) + int(var_vertex_nm))): #rotated vertexen, with original color code
        outfile2.write('%s\n'%(line2))
        g += 1
        
    elif (int(var_header) + int(var_vertex_nm)) == d: #for new vertexen, with color code 0,0,0
        outfile2.write('%s\n'%(line2)) #the last original vertex
        g += 1
        
        for a in range(0, len(co)): # the new vertexen, with color code
            getal = float(co[a][0])
            co[a][0] = (getal * -1)
    
            #print co[a][0]
            outfile2.write('%s %s %s 230 0 182\n'%(co[a][0], float(co[a][1]), float(co[a][2])))
            g += 1
                                            
        
    else: #everything left
        outfile2.write('%s\n'%(line2))


 
print 'writing points to outputfile'
#writing points to outputfile
for z in range(0,len(C)):
    point1 = C[z][0]
    point2 = C[z][1]
    point3 = C[z][2]
    indexthing1 = co.index(C[z][0])
    indexthing2 = co.index(C[z][1])
    indexthing3 = co.index(C[z][2])
    output.write("3 %s %s %s\n"%((indexthing1), (indexthing2), (indexthing3)))
    outfile2.write("3 %s %s %s\n"%((indexthing1 + int(var_vertex_nm)), (indexthing2 + int(var_vertex_nm)), (indexthing3 + int(var_vertex_nm))))
output.close() 
outfile2.close()
number_extra_faces = len(C)
number_extra_co = len(co)

