import math
from math import *
import sys
import numpy
from time import gmtime, strftime

def time():
    a = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
    return a

def user_input_side(out_log): # user input side 
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
    return side

def user_input_sections(out_log): # user input sections 
    # number of boxes on x axis, this will be multiplied. 
    number_of_boxes_hor = int(raw_input("number_of_boxes on x axis: "))
    # number of boxes on y axis
    number_of_boxes_ver = int(raw_input("number_of_boxes on y axis: "))
    # number of boxes on z axis
    number_of_boxes_z = int(raw_input("number_of_boxes on z axis: "))
    out_log.write("number of boxes x axis:\t%s\nnumber of boxes y axis:\t%s\nnumber of boxes z axis:\t%s\n\n"%((number_of_boxes_hor *2),(number_of_boxes_ver), (number_of_boxes_z)))

    return number_of_boxes_hor, number_of_boxes_ver, number_of_boxes_z

def user_input_colors(out_log): # color of reconstructed surface
    while True:
        col = raw_input("color faces: Pink (0) Blue (1):  ").upper().strip()
        col.strip()
        if int(col) == 0:
            out_log.write('color is pink\n')
            col_r = 236
            col_g = 149
            col_b = 221
            break
        elif int(col) == 1:
            out_log.write('color is blue\n')
            col_r = 192
            col_g = 245
            col_b = 250
            break
        elif int(col) == 2:
            out_log.write('color is green\n')
            col_r = 0
            col_g = 255
            col_b = 0
            break
        elif int(col) == 3:
            out_log.write('color is red\n')
            col_r = 255
            col_g = 0
            col_b = 0
            break
        else:
            print 'not the right input, try again'

    return col_r, col_g, col_b


def user_input_factor_stdev(out_log): # factor standard deviation
    factor = int(raw_input("factor of standard deviation (standard 1): "))
    out_log.write("Factor standard deviation:\t%s\n\n"%(factor))

    return factor


def extracting_header(file_ply):  # extracting header of ply file
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
    file_ply.close()

    return var_header, var_vertex_ln,var_vertex_nm,var_face_ln,var_face_nm


def array_coordinates(name_file_ply, var_vertex_nm, var_header,var_face_nm): # extracting coordinates of input file
    file1 = open(name_file_ply)
    matrix = numpy.zeros((int(var_vertex_nm),3)) # creating empty numpy array of amount of vertexen 
    matrix2 = numpy.empty((int(var_face_nm),3)) # creating empty numpy array of amount of faces

    count = 0 # counter for vertexen
    count2 = 0 # counter for faces
    # Putting all the vertexen and faces in a matrix
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
            
            if len(line) == 5: ########
                check2 = True
                #
    file1.close()

    return matrix,matrix2

def calc_histogram(matrix): # histogram of x,y, z coordinates
    x_co =  numpy.array(matrix[:,0])
    histo_x = numpy.histogram(x_co, bins = 100)
    y_co =  numpy.array(matrix[:,1])
    histo_y = numpy.histogram(y_co, bins = 100)
    z_co =  numpy.array(matrix[:,2])
    histo_z = numpy.histogram(z_co, bins = 100)

    return histo_x,histo_y,histo_z
    

def calc_min_max(out_log, matrix): # minima and maxima of x,y and z
    amin = numpy.amin(matrix, axis = 0) #minima of x y and z
    amax = numpy.amax(matrix, axis = 0) #maxima of x y and z

    out_log.write("lowest x:\t%s\nhighest x:\t%s\nlowest y:\t%s\nhighest y:\t%s\nlowest z:\t%s\nhighest z:\t%s\n\n"
                  %(amin[0],amax[0],amin[1],amax[1],amin[2],amax[2]))

    return amin, amax


def range_sections(amin,amax,number_of_boxes_hor, number_of_boxes_ver,number_of_boxes_z):# Calculating range for sections 
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

    return steps_x, steps_y, steps_z, x_window_min_x,x_window_max_x

def create_list_ranges(amin,amax,number_of_boxes_hor, number_of_boxes_ver,number_of_boxes_z,
                       x_window_min_x, x_window_max_x,steps_x,steps_y,steps_z): # creat list with ranges of each section
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

    return newlist

def create_list_coordinates(newlist): # create list coordinates in sections
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
        
    return newlist2, indexlist

def fill_sections_coordinates(newlist,newlist2,matrix,indexlist): # fill list sections with coordinates
    #Filling the boxes with the coordinates
    for y in range(0,len(newlist2)): #notice the ranges are in reverse order of each box
        rows_vertex = (numpy.where((matrix[:,0]>= float(newlist2[y][5]))
                        & (matrix[:,0] < float(newlist2[y][4]))
                        & (matrix[:,1] >= float(newlist2[y][3]))
                        & (matrix[:,1] < float(newlist2[y][2]))
                        & (matrix[:,2] >= float(newlist2[y][1]))
                        & (matrix[:,2] < float(newlist2[y][0]))))
        
        vertex_new = matrix[list(rows_vertex)]
        newlist[y].append((vertex_new))
        indexlist[y].append((rows_vertex))
        
    return newlist, indexlist


def calc_sections(number_of_boxes_ver,number_of_boxes_hor,number_of_boxes_z,newlist): # calculate mean and number of coordinates sections 
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
    
        first_pos = (newlist[counter2][0]) # coordinates of left box
        last_pos = (newlist[counter2 + (int(number_of_boxes_hor)*2 -1)- counter][0]) # coordinates of right box
        if len(first_pos) == 0: # If there are no coordinates in a box
            number_coordinates_box1 = len(first_pos)
            mean1 = 2000 
            mean3 = '' 

        else:
            number_coordinates_box1 = len(first_pos) # deze kunnen eruit 
            for e in range(0,len(first_pos)): # If there are coordinates in a box
                total += float(first_pos[e][0])
            mean1 = total/len(first_pos)
            mean3 = mean1
            total = 0

        if len(last_pos) == 0: # If there are no coordinates in a box
            number_coordinates_box2 = len(last_pos)
            mean2 = 1000 
            mean4 = ''

        else:
            number_coordinates_box2 = len(last_pos)
             
            for e in range(0,len(last_pos)): # If there are coordinates in a box
                total += float(last_pos[e][0])
            mean2 = total/len(last_pos)
            mean4 = mean2
            total = 0
        number_coordinates_box1 = len(first_pos)
        number_coordinates_box2 = len(last_pos)

        if (abs(number_coordinates_box1 - number_coordinates_box2) > (number_coordinates_box1 / 2.0)) and(abs(number_coordinates_box1 - number_coordinates_box2) > (number_coordinates_box2 / 2.0)):
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

    return difference, differencemean


def calc_mean_stdev(differencemean, factor):    # Calculating the mean and the standard deviation
    mean_percentage = numpy.mean(differencemean) #calculating the mean without empty boxes
    std_percentage = numpy.std(differencemean) # calculating the standard deviation of the list without the empty boxes
    std_percentage = std_percentage * factor

    return mean_percentage, std_percentage

def calc_range(mean_percentage,std_percentage): #calculate the left and right range of accepted differences
    left_range = float(mean_percentage) - float(std_percentage) #left range mean minus one standard deviation
    right_range = float(mean_percentage) + (float(std_percentage) )# right range mean plus one standard deviation
    if left_range > 0:
        left_range = 0
    return left_range, right_range

def collect_mirror_values(out_log, side, output, right_range, left_range,mean_percentage,
                          std_percentage, newlist, indexlist,difference,
                          number_of_boxes_hor,number_of_boxes_ver,number_of_boxes_z,
                          col_r, col_g, col_b): # collect wrong coordinates
    
    # Collecting the values of the sections which have to be mirrored
    out_log.write('mean x difference:\t%s\nstandarddeviation mean x difference:\t%s\nrange:\t%s - %s\n\n'%
                  ((mean_percentage),(std_percentage),(left_range),(right_range)))
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
                if len(newlist[counter2 -1][0]) != 0:
                    sub = (newlist[counter2 -1][0]) #coordinates in list
                    for y in range(0, len(sub)):
                        i = sub[y]
                        index_a = indexlist[counter2 -1][0][0][y]
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
                        output.write('%s %s %s %s %s %s\n'%(sub[y][0], float(sub[y][1]), float(sub[y][2]),(col_r), (col_g), (col_b))) # writing new coordinates to output
               
       
        # if the right side of the object is correct
        if side == 1:
            dif = (int(number_of_boxes_hor)) - counter
            counter3 = counter2 + (dif*2) + 1 # right side counter

            if (float(difference[x] )> float(right_range)) or (float(difference[x]) < float(left_range)):
                if len(newlist[counter3 -1][0]) != 0:
                    sub = (newlist[counter3 -1][0]) # coordinates in list
                    for y in range(0, len(sub)):
                        i = sub[y]
                        index_a = indexlist[counter3 -1][0][0][y]
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
                        output.write('%s %s %s %s %s %s\n'%(sub[y][0], float(sub[y][1]), float(sub[y][2]),(col_r), (col_g), (col_b))) # writing new coordinates to output

    return total, listindexcount, listindex, listindextotalcount,totalcount

def find_original_faces(matrix2, listindex): # find original faces for corrected coordinates
    # finding the original faces of kopied points
    listfacessub = []
    listfaces = []
    listpoint = []
    a = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
    ix = numpy.in1d(matrix2.ravel(),listindex).reshape(matrix2.shape) # finding where the listindex is the same as the matrix
    rows, cols = numpy.where(ix) # finding index of the faces
    oi = matrix2[list(set(rows))] # extracting the rows with those faces

    return oi


def replace_index_values(oi,listindex,listindextotalcount): # Replacing the index values
    c = []
    array_oi = numpy.array(oi)
    maxn = numpy.amax(array_oi)
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
            key2.append(litc_sorted[counter])
            counter += 1
        else:
            key2.append(numpy.nan)
            
    key2 = numpy.array(key2) # converten of list to array
    index_f = numpy.digitize(array_oi.reshape(-1,), palette2)-1 # indexing which numbers has to be changed
    outb =(key2[index_f].reshape(array_oi.shape)) # new array creating with changed values?
    outc = outb[~numpy.isnan(outb).any(axis=1)] # extracting the faces with not changed values, (nan)

    return outc


def write_output(name_file_ply, out_log, totalcount, var_header, var_vertex_nm, var_face_nm,outc): # write output 
    outfile2 = open('final_output.ply', 'w')#writing the output file
    file1 = open(name_file_ply)
    g = 0
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
        outfile2.write("3 %s %s %s\n"%((int(outc[z][0])+ int(var_vertex_nm)),
                                       (int(outc[z][1])+ int(var_vertex_nm)), (int(outc[z][2])+ int(var_vertex_nm))))

    out_log.write('number of reconstructed faces:\t%s\n\n'%(len(outc)))    
    outfile2.close()

                 
def main():
    var_col = 0
    name_file_ply = 'outfile_rotating2.ply' 
    output = open('new_coordinates2.ply', 'w')
    file_ply = open(name_file_ply)
    out_log = open('log_reConstructor.txt', 'w')

    out_log.write('Start time: %s\n\nInput user:\n'%(time()))
    # user input side
    side = user_input_side(out_log)
    # user input sections
    number_of_boxes_hor,number_of_boxes_ver,number_of_boxes_z = user_input_sections(out_log)
    # user input factor stdev
    factor = user_input_factor_stdev(out_log)
    # user input colors
    col_r, col_g, col_b = user_input_colors(out_log)
    # extracting header
    var_header, var_vertex_ln,var_vertex_nm,var_face_ln,var_face_nm = extracting_header(file_ply)
    # array coordinates
    matrix, matrix2 = array_coordinates(name_file_ply, var_vertex_nm, var_header, var_face_nm)
    # calc min max
    amin,amax = calc_min_max(out_log, matrix)
    # calc histogram
    histo_x,histo_y,histo_z = calc_histogram(matrix)
    # range sections
    steps_x,steps_y,steps_z,x_window_min_x,x_window_max_x = range_sections(amin,amax,
                                                                           number_of_boxes_hor, number_of_boxes_ver,
                                                                           number_of_boxes_z)
    # create list ranges
    newlist = create_list_ranges(amin,amax,number_of_boxes_hor, number_of_boxes_ver,
                                 number_of_boxes_z, x_window_min_x, x_window_max_x,steps_x,steps_y,steps_z)
    # create list coordinates
    newlist2, indexlist = create_list_coordinates(newlist)
    # fill sections coordinates
    newlist, indexlist = fill_sections_coordinates(newlist, newlist2, matrix, indexlist)
    # calc sections
    difference, differencemean = calc_sections(number_of_boxes_ver,number_of_boxes_hor,number_of_boxes_z,newlist)
    # calc mean stdec
    mean_percentage, std_percentage = calc_mean_stdev(differencemean,factor)
    # calc range
    left_range, right_range = calc_range(mean_percentage,std_percentage)
    # collect mirror values
    total, listindexcount, listindex, listindextotalcount, totalcount = collect_mirror_values(out_log, side, output,
                                                                                              right_range, left_range,
                                                                                              mean_percentage, std_percentage,
                                                                                              newlist, indexlist,  difference,
                                                                                              number_of_boxes_hor,number_of_boxes_ver,number_of_boxes_z,
                                                                                              col_r, col_g, col_b)

    # find origial faces
    oi = find_original_faces(matrix2, listindex)
    # replace index values
    outc = replace_index_values(oi,listindex,listindextotalcount)

    output.close()
    # write output
    write_output(name_file_ply, out_log, totalcount, var_header, var_vertex_nm, var_face_nm,outc)
    a = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
    
    out_log.write('End time: %s'%(a))
    out_log.close()
    
main()



