#second part of face creation program
#calculating if points are correct,then correcting the  newpoints
import math
from math import *
import sys
import numpy

print numpy.__version__
#Start time
from time import gmtime, strftime
a = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
print a 

var_col = 0
#name_file_ply = raw_input("Rotated ply file: ") #dta file
name_file_ply = 'outfile_rotating2.ply' #
output = open('new_coordinates2.ply', 'w')
file_ply = open(name_file_ply)
out_log = open('log_reConstructor.txt', 'w')
#Input user for identify which side is correct
out_log.write('Start time: %s\n\nInput user:\n'%(a))
while True:
    side = raw_input("left side of object is correct:(Yes or No):  ").upper().strip()
    side.strip()
    if side == 'YES' or side == 'Y':
        out_log.write('Left side of object is correct:\t%s\n\n'%(side))
        side = 0
        break
    elif side == 'NO' or side == 'N':
        out_log.write('Left side of object is correct:\t%s\n\n'%(side))
        side = 1
        break
    else:
        print 'not the right input, try again'


# Input user for deviding object in squares.
number_of_boxes_hor = int(raw_input("number_of_boxes on x axis: ")) # number of boxes on x axis, this will be multiplied. 
number_of_boxes_ver = int(raw_input("number_of_boxes on y axis: ")) # number of boxes on y axis
number_of_boxes_z = int(raw_input("number_of_boxes on z axis: ")) # number of boxes on z axis
factor = int(raw_input("factor of standard deviation (standard 1): "))
out_log.write("Factor standard deviation:\t%s\n\n"%(factor))
print number_of_boxes_hor *2, 'number_of_boxes_x'
print number_of_boxes_ver, 'number_of_boxes_y'
print number_of_boxes_z, 'number_of_boxes_z'
out_log.write("number of boxes x axis:\t%s\nnumber of boxes y axis:\t%s\nnumber of boxes z axis:\t%s\n\n"%((number_of_boxes_hor *2),(number_of_boxes_ver), (number_of_boxes_z)))
#extracting the header
for x in range(0, 20):
    readheader = file_ply.readline().strip().split()
    print readheader
    if readheader[0] == 'end_header': # when the words 'end_header' are found
        var_header = x # var_header is line number
    if readheader[0] == "element" and readheader[1] == "vertex": # when 'element vertex' found
        var_vertex_ln = readheader[1] # line number of element vertex
        var_vertex_nm = readheader[2] # amount of vertexen
    if readheader[0] == "element" and readheader[1] == "face": # when 'element face' found
        var_face_ln = readheader[1] # line number of element face
        var_face_nm = readheader[2] # amount of faces

print 'end header'

file_ply.close() # closing the input file

print 'filling the array with the coordinates'
file1 = open(name_file_ply) # open the input file second time

matrix = numpy.zeros((int(var_vertex_nm),3)) # creating empty numpy array of amount of vertexen 
matrix2 = numpy.empty((int(var_face_nm),3)) # creating empty numpy array of amount of faces

count = 0 # counter for vertexen
count2 = 0 # counter for faces
# Putting alle the vertexen and faces in a matrix
for a in range(0, (int(var_header) + int(var_vertex_nm) + int(var_face_nm) + 1)):
    line = file1.readline().strip().split() # reading every line
    if int(var_header) < a < (int(var_vertex_nm)+ int(var_header)+1): #vertexen
        matrix[count][0] = float(line[0]) # x coordinate
        matrix[count][1] = float(line[1]) # y coordinate
        matrix[count][2] = float(line[2]) # z coordinate
        count += 1 # counter + 1 for next line in matrix
    if a > (int(var_vertex_nm)+ int(var_header)): # faces
        if len(line) == 4:
            matrix2[count2][0] = int(line[1]) # first coordinate for face
            matrix2[count2][1] = int(line[2]) # second coordinate for face
            matrix2[count2][2] = int(line[3]) # third coordinate for face
            check1 = True
        count2 += 1 # counter + 1 for next line in matrix
        if len(line) == 5: # hier nog wat op verzinnen!!!! voor als er faces zijn met 4
            check2 = True
print 'end xyz coordinates to array'
numpy.set_printoptions(threshold='nan')

#Calculating the max and min of x, y and z
amin = numpy.amin(matrix, axis = 0) #minima of x y and z
amax = numpy.amax(matrix, axis = 0) #maxima of x y and z

print "lowest_x: %s"%(amin[0])
print "highest_x: %s"%(amax[0])
print "lowest_y: %s"%(amin[1])
print "highest_y: %s"%(amax[1])
print "lowest_z: %s"%(amin[2])
print "highest_z: %s"%(amax[2])

out_log.write("lowest x:\t%s\nhighest x:\t%s\nlowest y:\t%s\nhighest y:\t%s\nlowest z:\t%s\nhighest z:\t%s\n\n"%(amin[0],amax[0],amin[1],amax[1],amin[2],amax[2]))


# Calculating range for boxes

# Find the highest absolute x because the boxes on x axis has mirrored in the symmetry plane
if abs(amax[0]) < abs(amin[0]): # if the highest x is absolute smaller than the lowest x:
    x_window_min_x = amin[0] # lowest x is lowest windows x
    x_window_max_x= amin[0] *-1 # lowest x * -1 is highest windows x 
    steps_x = abs(amin[0]) / number_of_boxes_hor # length of x boxes
else:
    x_window_min_x = amax[0] *-1 # highest x *-1 is lowest windows x
    x_window_max_x = amin[0] # highest x is highest window x
    steps_x = abs(amax[0]) / number_of_boxes_hor # length of x boxes

#Calculating range of y boxes
steps_y = (abs(amax[1]) + abs(amin[1])) / number_of_boxes_ver

#Calculating range of z boxes
steps_z = (abs(amax[2]) + abs(amin[2])) / number_of_boxes_z


print steps_y, 'steps_y'
print steps_x, 'steps_x'
print steps_z, 'steps_z'

#creating the list with the ranges for every box

y_window_min = amin[1]
y_window_max = amin[1]
z_window_min = amin[2]
newlist = []
sublist = []
y_window_min2 = y_window_min
z_window_min2 = z_window_min

# From front to back, from floor to ceiling
for a in range(0,int(number_of_boxes_ver)): #number of rows
    x_window_min = x_window_min_x
    x_window_min2 = x_window_min_x + steps_x
    y_window_min = y_window_min2
    y_window_min2+= steps_y
    z_window_min = amin[2]
    z_window_min2 = z_window_min
    for c in range(0,int(number_of_boxes_z)): # in z direction
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

# creating empty index list for storing line index of coordinates
indexlist = []
for x in range(0,len(newlist)):
    indexlist.append([])

print 'filling the new list with the coordinates for each box'

#Filling the boxes with the coordinates
for x in range(0,int(var_vertex_nm)):
    for y in range(0,len(newlist2)): #notice the ranges are in reverse order of each box
        if float(matrix[x][0]) >= float(newlist2[y][5]) and float(matrix[x][0]) < float(newlist2[y][4]) and float(matrix[x][1]) >= float(newlist2[y][3]) and float(matrix[x][1]) < float(newlist2[y][2]) and float(matrix[x][2]) >= float(newlist2[y][1]) and float(matrix[x][2]) < float(newlist2[y][0]):
            newlist[y].append(matrix[x]) # store coordinates in right box
            indexlist[y].append(x) # store line index of coordinate in box


#Selecting the boxes on the symmetry axis and calculating the mean of every box
counter = 0
counter2 = 0
counter3 = 0
row_count = 0
difference = [] #whit boxes who are empty, the empty ones get the number 0
differencemean = [] # is without boxes who are empty
total = 0
for x in range(0, (int(number_of_boxes_ver)*int(number_of_boxes_hor) * int(number_of_boxes_z))): # through all the lists/boxes
    if counter % (int (number_of_boxes_hor)*2) == 0: 
        counter = 0
    if counter3 == (int(number_of_boxes_hor)):
        counter2 += (int(number_of_boxes_hor))
        counter3 = 0
    
    first_pos = newlist[counter2] # coordinates of left box
    last_pos = newlist[counter2 + (int(number_of_boxes_hor)*2 -1)- counter] # coordinates of right box
    if len(first_pos) == 0: # If there are no coordinates in a box
        number_coordinates_box1 = len(first_pos)
        mean1 = 2000 # random number
        mean3 = '' 
    else:
        number_coordinates_box1 = len(first_pos) # deze kunnen eruit
        #print number_coordinates_box1, '1' 
        for e in range(0,len(first_pos)): # If there are coordinates in a box
            total += float(first_pos[e][0])
        mean1 = total/len(first_pos)
        mean3 = mean1
        total = 0
    if len(last_pos) == 0: # If there are no coordinates in a box
        number_coordinates_box2 = len(last_pos)
        mean2 = 1000 # random number
        mean4 = ''
    else:
        number_coordinates_box2 = len(last_pos)
        #print number_coordinates_box2, '2\n' 
        for e in range(0,len(last_pos)): # If there are coordinates in a box
            total += float(last_pos[e][0])
        mean2 = total/len(last_pos)
        mean4 = mean2
        total = 0
        
    if (abs(number_coordinates_box1 - number_coordinates_box2) > (number_coordinates_box1 / 3.0)) and  (abs(number_coordinates_box1 - number_coordinates_box2) > (number_coordinates_box2 / 3.0)):
        #print number_coordinates_box1, '1\t' , number_coordinates_box2, '2t\n'
        
        mean1 = 3000
        mean2 = 4000

    difference.append(float(abs(mean2 + mean1))) #the means of every boxes
    counter += 2
    counter2 += 1
    counter3 += 1
    try:
        differencemean.append(abs(mean4 + mean3)) # the mean without empty boxes
    except:
        continue
 
# Calculating the mean and the standard deviation
mean_percentage = numpy.mean(differencemean) #calculating the mean without empty boxes
print mean_percentage, 'mean percentage'
print len(differencemean), 'len differencemean'
std_percentage = numpy.std(differencemean) # calculating the standard deviation of the list without the empty boxes
print std_percentage, 'std'
std_percentage = std_percentage * factor
# Calculating the left and right acceptable mean x
left_range = float(mean_percentage) - float(std_percentage) #left range mean minus one standard deviation
right_range = float(mean_percentage) + (float(std_percentage) )# right range mean plus one standard deviation

print 'right range', right_range
print 'left range', left_range
if left_range > 0:
    left_range = 0
# Collecting the values of the boxes which have to be mirrored
out_log.write('mean x difference:\t%s\nstandarddeviation mean x difference:\t%s\nrange:\t%s - %s\n\n'%((mean_percentage),(std_percentage),(left_range),(right_range)))
y = 0
counter = 0
counter2 = 0
sub = []
total = []
left_range = "%.10f"%(left_range)
indexcount = 0
facecount = 0
totalcount = 0
listindex = []
listindexsub = []
listindexcount = []
listindextotalcount = []
print 'find wrong coordinates'
for x in range(0, len(difference)):
    difference_x = "%.10f"%(difference[x])
    if counter %(int(number_of_boxes_hor)) == 0 and x != 0:
        counter = 0
        counter2 += (int(number_of_boxes_hor))
    counter += 1
    counter2 += 1 #left side counter 
    # if left side of the object is correct
    if side == 0:
        if (float(difference_x) < float(left_range)) or (float(difference_x) > float(right_range)):
            if len(newlist[counter2 -1]) != 0:
                sub = (newlist[counter2 -1]) #coordinates in list
                for y in range(0, len(sub)):
                    i = sub[y]
                    index_a = indexlist[counter2 -1][y]
                    try:
                        listindex.append(int(index_a)) # index number
                        listindextotalcount.append(int(totalcount))
                        listindexsub.append(int(index_a)) # index number
                        listindexsub.append(totalcount) # index number of new coordinate 

                    except:
                        continue
                    listindexcount.append(listindexsub) # index number original
                    listindexsub = []
                    getal= float(sub[y][0]) * -1 # x coordinate * -1 for mirroring at symmetry plane
                    sub[y][0] = getal
                    total.append(sub[y])
                    totalcount += 1
                    output.write('%s %s %s 230 0 %s \n'%(sub[y][0], float(sub[y][1]), float(sub[y][2]),(x+60))) # writing new coordinates to output
           
   
    # if the right side of the object is correct
    if side == 1:
        dif = (int(number_of_boxes_hor)) - counter
        counter3 = counter2 + (dif*2) + 1 # right side counter

        if (float(difference[x] )> float(right_range)) or (float(difference[x]) < float(left_range)):
            if len(newlist[counter3 -1]) != 0:
                sub = (newlist[counter3 -1]) # coordinates in list
                for y in range(0, len(sub)):
                    i = sub[y]
                    index_a = indexlist[counter3 -1][y]
                    try:
                        listindex.append(int(index_a))# index number
                        listindextotalcount.append(int(totalcount))
                        listindexsub.append(int(index_a)) # index number
                        listindexsub.append(totalcount)# index number of new coordinate 
                    except:
                        continue
                    listindexcount.append(listindexsub)# index number original
                    listindexsub = []
                    getal= float(sub[y][0]) * -1 # x coordinate * -1 for mirroring at symmetry plane
                    sub[y][0] = getal
                    total.append(sub[y])
                    totalcount += 1
                    output.write('%s %s %s 150 0 %s \n'%(sub[y][0], float(sub[y][1]), float(sub[y][2]),(x+60))) # writing new coordinates to output


a = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
print a 

# finding the original faces of kopied points
print 'find faces with coordinates in it'
listfacessub = []
listfaces = []
listpoint = []
print 'start find face'
a = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
print a 
ix = numpy.in1d(matrix2.ravel(),listindex).reshape(matrix2.shape) # finding where the listindex is the same as the matrix
rows, cols = numpy.where(ix) # finding index of the faces
oi = matrix2[list(set(rows))] # extracting the rows with those faces
a = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
print a 
print 'end find face'

output.close()


a = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
print a

# Replacing the index values
outfile2 = open('final_output.ply', 'w')
print 'replace the values of index for the right ones'
c = []
array_oi = numpy.array(oi)

maxn = numpy.amax(array_oi)
print 'max', maxn
palette = list(range(int(maxn)))
palette = numpy.array(palette)
key = numpy.array(listindex)
listindextotalcount = numpy.array(listindextotalcount)

# sorting the lists which have to be replaced
order= numpy.argsort(key) # sorting of the array key 
litc_sorted = listindextotalcount[order] # sorting the palette
key_sorted = key[order] # sorting the key

palette2 = list(range(int(maxn))) # creating list with all possible values in it with max the highest number in the faces
key2 = []

counter = 0
for x in range(0,int(maxn)): # make array where in is what have to be changed
    if (counter < len(key_sorted)) and x == (key_sorted[counter]):
        #print counter, key_sorted[counter]
        key2.append(litc_sorted[counter])
        counter += 1
    else:
        key2.append(numpy.nan)

key2 = numpy.array(key2) # converten of list to array
index_f = numpy.digitize(array_oi.reshape(-1,), palette2)-1 # indexing which numbers has to be changed?
outb =(key2[index_f].reshape(array_oi.shape)) # new array creating with changed values?
outc = outb[~numpy.isnan(outb).any(axis=1)] # extracting the faces with not changed values, (nan)

#writing the output file
file1.close()
file1 = open(name_file_ply)
g = 0
print 'totalcount', totalcount
for d in range(0,(int(var_header) + int(var_vertex_nm) + int(var_face_nm) + 1)):
    line2 = file1.readline().strip()
    readline2 = line2.strip().split()
    if readline2[0] == "element" and readline2[1] == "vertex":
        outfile2.write("element vertex %s\n"%(int(var_vertex_nm) + totalcount)) #number of vertexen changing
                       
    elif readline2[0] == "element" and readline2[1] == "face":
        outfile2.write("element face %s\n"%(int(var_face_nm) + len(outc)))#number of faces changing                                      
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

#writing new faces to output
for z in range(0,len(outc)):
    outfile2.write("3 %s %s %s\n"%((int(outc[z][0])+ int(var_vertex_nm)), (int(outc[z][1])+ int(var_vertex_nm)), (int(outc[z][2])+ int(var_vertex_nm))))

out_log.write('number of reconstructed faces:\t%s\n\n'%(len(outc)))    
output.close()
outfile2.close()
    

a = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
print a
out_log.write('End time: %s'%(a))
out_log.close()
