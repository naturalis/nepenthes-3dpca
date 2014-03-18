#second part of face creation program
#calculating if points are correct. 
import math
from math import *
import sys
import numpy
from scipy.spatial import cKDTree

from time import gmtime, strftime
a = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
print a 

name_file_ply = 'outfile_rotating2.ply'
output = open('new_coordinates2.ply', 'w')
file_ply = open(name_file_ply)

var_col = 0
site = 1 #MOET NOG VERANDERD WORDEN = 0 = links

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
        var_face_nm = readheader[2] #number of faces

print var_vertex_nm, 'dit'
listtotal_colors = []
sub_colors = []
print 'end header'

file_ply.close()
file1 = open(name_file_ply)
matrix = numpy.zeros((int(var_vertex_nm),3)) #creating empty numpy array. 

#filling the array with the coordinates
count = 0
for a in range(0, (int(var_header) + int(var_vertex_nm) + int(var_face_nm) + 1)):
    line = file1.readline().strip().split()
    if int(var_header) < a < (int(var_vertex_nm)+ int(var_header)+1):
        matrix[count][0] = line[0]
        matrix[count][1] = line[1]
        matrix[count][2] = line[2]
        count += 1

print 'end xyz coordinates to array'


#calculating the max and min of x, y and z
amin = numpy.amin(matrix, axis = 0) #minima of x y and z
amax = numpy.amax(matrix, axis = 0) #maxima of x y and z


#total number of points divided by the window of y
number_points_y_range = float(var_vertex_nm) / (amax[1] - amin[1])
print 'number of points in  y range: %s'%(number_points_y_range)
rangenm = float(var_vertex_nm)/ 10#moet die 100000 zijn?4
print 'rangenm', rangenm

print "lowest_x: %s"%(amin[0])
print "highest_x: %s"%(amax[0])
print "lowest_y: %s"%(amin[1])
print "highest_y: %s"%(amax[1])
print "lowest_z: %s"%(amin[2])
print "highest_z: %s"%(amax[2])


number_of_boxes_ver = 6 # dit moet nog anders
number_of_boxes_hor = 4
number_of_boxes_z = 4


if abs(amax[0]) < abs(amin[0]):
    x_window_min_x = amin[0]
    x_window_max_x= amin[0] *-1
    steps_x = abs(amin[0]) / number_of_boxes_hor
else:
    x_window_min_x = amax[0] *-1
    x_window_max_x = amin[0]
    steps_x = abs(amax[0]) / number_of_boxes_hor
steps_y = (abs(amax[1]) + abs(amin[1])) / number_of_boxes_ver
steps_z = (abs(amax[2]) + abs(amin[2])) / number_of_boxes_z
print number_of_boxes_ver, 'number_of_boxes_ver'
print number_of_boxes_hor *2, 'number_of_boxes_hor'
print number_of_boxes_z, 'number_of_boxes_z'
print steps_y, 'steps_y'
print steps_x, 'steps_x'
print steps_z, 'steps_z'
#creating the list with the ranges

y_window_min = amin[1]
y_window_max = amin[1]
z_window_min = amin[2]
newlist = []
sublist = []


y_window_min2 = y_window_min
z_window_min2 = z_window_min

for a in range(0,int(number_of_boxes_ver)): #number of rows
    x_window_min = x_window_min_x
    x_window_min2 = x_window_min_x + steps_x
    y_window_min = y_window_min2
    y_window_min2+= steps_y
    z_window_min = amin[2]
    z_window_min2 = z_window_min
    for c in range(0,int(number_of_boxes_z)):
        z_window_min = z_window_min2
        z_window_min2 += steps_z
        x_window_min = x_window_min_x
        x_window_min2 = x_window_min_x + steps_x
        for b in range(0, int((2*number_of_boxes_hor))): #number of columns 
            sublist.append(x_window_min)
            sublist.append(x_window_min2)
            sublist.append(y_window_min)
            sublist.append(y_window_min2)
            sublist.append(z_window_min)
            sublist.append(z_window_min2)
            newlist.append(sublist)
            sublist = []
            x_window_min = x_window_min2
            x_window_min2 += steps_x

#empty the list but maintaining the structure   
newlist2=[]
newlist2sub = []
newlistsub = []


for x in range(0,len(newlist)):
    for y in range(5,-1,-1):
        newlist2sub.append(newlist[x].pop(y))
    newlist2.append(newlist2sub)
    newlist2sub = []

#filling the new list with the coordinates for each box
for x in range(0,int(var_vertex_nm)):
    #if x%1000 == 0:
        #print x
        
    for y in range(0,len(newlist2)): #notice the ranges are in reverse order of each box
        if float(matrix[x][0]) >= float(newlist2[y][5]) and float(matrix[x][0]) < float(newlist2[y][4]) and float(matrix[x][1]) >= float(newlist2[y][3]) and float(matrix[x][1]) < float(newlist2[y][2]) and float(matrix[x][2]) >= float(newlist2[y][1]) and float(matrix[x][2]) < float(newlist2[y][0]):
            newlist[y].append(matrix[x])

#Selecting the boxes on the symmetry axis and calculating the mean of every box
counter = 0
counter2 = 0
counter3 = 0
row_count = 0
meanlist = []
difference = [] #whit boxes who are empty, the empty ones get the number 0
differencemean = [] # is without boxes who are empty
total = 0
for x in range(0, (int(number_of_boxes_ver)*int(number_of_boxes_hor) * int(number_of_boxes_z))):
    if counter % (int (number_of_boxes_hor)*2) == 0:
        counter = 0
    if counter3 == (int(number_of_boxes_hor)):
        counter2 += (int(number_of_boxes_hor))
        counter3 = 0
    
    eerste_pos = newlist[counter2]
    laatste_pos = newlist[counter2 + (int(number_of_boxes_hor)*2 -1)- counter]
    if len(eerste_pos) == 0:
        mean1 = 2000 # hier moet nog wat anders voor komen.
        mean3 = ''
    else:
        for e in range(0,len(eerste_pos)):
            total += float(eerste_pos[e][0])
        mean1 = total/len(eerste_pos)
        mean3 = mean1
        total = 0
    if len(laatste_pos) == 0: #this has to be changed
        mean2 = 1000
        mean4 = ''
    else:
        for e in range(0,len(laatste_pos)):
            total += float(laatste_pos[e][0])
        mean2 = total/len(laatste_pos)
        mean4 = mean2
        total = 0
    
    difference.append(float(abs(mean2 - mean1)))
    counter += 2
    counter2 += 1
    counter3 += 1
    try:
        differencemean.append(abs(mean4 - mean3))
    except:
        continue
    
#print difference  
mean_percentage = numpy.mean(differencemean) #calculating the mean without empty boxes
print mean_percentage, 'mean percentage'
print len(differencemean), 'len differencemean'
std_percentage = numpy.std(differencemean) # calculating the standard deviation of the list without the empty boxes
print std_percentage, 'std'

left_range = float(mean_percentage) - float(std_percentage) #left range mean minus one standard deviation
right_range = float(mean_percentage) + (2* float(std_percentage) )# right range mean plus one standard deviation

if left_range > 0:
    left_range = 0.0

print 'right range', right_range
print 'left range', left_range

###### Collecting the values of the boxes which have to be mirrored
y = 0
counter = 0
counter2 = 0
sub = []
total = []
left_range = "%.10f"%(left_range)
print left_range

for x in range(0, len(difference)):
    difference_x = "%.10f"%(difference[x])
    # if left side is of the object is correct
    if counter %(int(number_of_boxes_hor)) == 0 and x != 0:
        counter = 0
        counter2 += (int(number_of_boxes_hor))
    counter += 1
    counter2 += 1 #left site counter 
    if site == 0:
        if (float(difference_x) < float(left_range)) or (float(difference_x) > float(right_range)):

            if len(newlist[counter2 -1]) != 0: #klopt dit?
                sub = (newlist[counter2 -1]) # -1 omdat je de posities telt van de lijst en de counter 1 tehoog is.
                for y in range(0, len(sub)):
                    getal= float(sub[y][0]) * -1
                    sub[y][0] = getal
                    total.append(sub[y])
                    output.write('%s %s %s 230 0 %s \n'%(sub[y][0], float(sub[y][1]), float(sub[y][2]),(x+60)))
           

    # if the right side of the object is correct
    if site == 1:
        dif = (int(number_of_boxes_hor)) - counter
        counter3 = counter2 + (dif*2) + 1 # right site counter
        if (difference[x] > right_range) or (difference[x] < left_range):
            if len(newlist[counter3 -1]) != 0: #klopt dit?
                sub = (newlist[counter3 -1]) # -1 omdat je de posities telt van de lijst en de counter 1 tehoog is.
                for y in range(0, len(sub)):
                    getal= float(sub[y][0]) * -1
                    sub[y][0] = getal
                    total.append(sub[y])
                    output.write('%s %s %s 150 0 %s \n'%(sub[y][0], float(sub[y][1]), float(sub[y][2]),(x+60)))
                
                
    

###calculating the triangle, nu is het nog alles bij elkaar, moet ik het opsplitsen in de boxjes?
# of moet ik een maximum distance neerzetten, zodat je niet rare dingen bij elkaar krijgt. 

data = numpy.array(total)
#print len(data)
#print data
tree = cKDTree(data)
#print tree
counter = 0
string_index =[]
output3 = open('outputsub.ply', 'w')
for x in data:
    dists, indexes = tree.query(numpy.array(x), k=3)

    for dist, index in zip(dists, indexes):
        if dist > 3:#moet nog wat anders op verzinnen, dat die niet hele grootte vlakken kan gaan maken.    
            break
        else:
            string_index.append(index)
    if len(string_index) == 3:
        counter += 3
        #output3.write('%s '%(3))
        output3.write('%s %s %s'%(string_index[0], string_index[1], string_index[2]))
        output3.write('\n')
    string_index = []


output.close()
output3.close()

outfile2 = open('final_output.ply', 'w')

#writing the output file
file1.close()
file1 = open(name_file_ply)
g = 0
for d in range(0,(int(var_header) + int(var_vertex_nm) + int(var_face_nm) + 1)):
    line2 = file1.readline().strip()
    readline2 = line2.strip().split()
    if readline2[0] == "element" and readline2[1] == "vertex":
        outfile2.write("element vertex %s\n"%(int(var_vertex_nm) + int(len(data)))) #number of vertexen changing
                       
    elif readline2[0] == "element" and readline2[1] == "face":
        outfile2.write("element face %s\n"%(int(var_face_nm) + counter/3))#number of vertexen changing                                      
    elif (int(var_header) < d < (int(var_header) + int(var_vertex_nm))): #rotated vertexen, with original color code
        outfile2.write('%s\n'%(line2))
        g += 1
        
    elif (int(var_header) + int(var_vertex_nm)) == d: #for new vertexen, with color code 0,0,0
        outfile2.write('%s\n'%(line2)) #the last original vertex
        g += 1
        with open('new_coordinates2.ply') as infile:
            for line in infile:
                outfile2.write(line)
                                            
        
    else: #everything left
        outfile2.write('%s\n'%(line2))

output3open = open('outputsub.ply')
for z in range(0, (counter/3)):
    line3 = output3open.readline().strip().split()
    outfile2.write("3 %s %s %s\n"%((int(line3[0]) + int(var_vertex_nm)), (int(line3[1])+ int(var_vertex_nm)), (int(line3[2])+ int(var_vertex_nm))))
    
output.close()
outfile2.close()
    

a = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
print a 
'''
#numpy arrays toevoegen! 
''' 
