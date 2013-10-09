#Mirna Baak
#Nepenthes pitchers project Naturalis Internship
#19-9-2013
#version 05
#last update: 9-10-2013

import operator
#Function input, for inputing files. 
def input_user():
    #name_file_dta = raw_input("dta_file: ")
    name_file_ply = raw_input("ply_file: ")
    #read_dta_file(name_file_dta)
    read_ply_file(name_file_ply)

# Function for reading dta file with 1 sample
def read_dta_file(name_file_dta):
    name_file_dta = name_file_dta
    open_file_dta = open(name_file_dta, 'r')
    length_total_file_dta = len(open_file_dta.readlines())
    open_file_dta.close()
    open_file2_dta = open(name_file_dta, 'r')
    x_co_dta = []   #x coordinates landmark list
    y_co_dta = []   #y coordinates landmark list
    z_co_dta = []   #z coordinates landmark list

    for x in range(0,length_total_file_dta):
        line_dta = open_file2_dta.readline().strip() # open data
        co_dta = line_dta.split('  ') #notice: 2 spaces 
        number_columns_dta = len(co_dta)    # number of columns on a line

        if x == 4:
            name_sample = line_dta  #name of sample
            
        if number_columns_dta == 3:
            x_co_dta.append('%s'%(float(co_dta[0])))    #list x_coordinate 
            y_co_dta.append('%s'%(float(co_dta[1])))    #list y_coordinate
            z_co_dta.append('%s'%(float(co_dta[2])))    #list x_coordinate

    
# Read file .ply 
def read_ply_file(name_file_ply):
    name_file_ply = name_file_ply
    #name_file_ply = raw_input("file: ")             # input name of file
    open_file = open(name_file_ply, 'r')            # open file
    length_total_file = len(open_file.readlines())  # total number of lines
    #print length_total_file
    open_file.close()                               # close file
    open_file2 = open(name_file_ply, 'r')           # open file second time

    f = open('output.ply', 'w')
    
    # seperate header
    header = ""
    for line in range(0,length_total_file):         # number of lines header
        data_line = open_file2.readline().strip()
        f.write("%s\n"%(data_line))
        if data_line == 'end_header':               # the end of the header
            header = header + data_line + "\n"
            break

        else:
            header = header + data_line + "\n"      # lines header
    print header

    
    x_co = []   #x coordinates list
    y_co = []   #y coordinates list
    z_co = []   #z coordinates list
    red = []    #red value list
    green = []  #green value list
    blue = []   #blue value list

    #random numbers
    y_max = -1000000
    y_min = 1000000
    x_max = -1000000
    x_min = 1000000 
    z_max = -1000000
    z_min = 1000000

    #x, y and z coordinates in seperate lists
    for line_2 in range(0, length_total_file):
        coordinates = open_file2.readline().strip() # readline input file
        split_tabs = coordinates.split(' ')         # split into seperate fragments for each line
        number_columns = len(split_tabs)            # number of columns on a line
        #print number_columns
        if number_columns == 6: ####
            x = float(split_tabs[0])            
            y = float(split_tabs[1])
            z = float(split_tabs[2])
            x_co.append('%s'%(x))   # list x coordinates
            y_co.append('%s'%(y))   # list y coordinates
            z_co.append('%s'%(z))   # list z coordinates
            #red.append('%s'%(split_tabs[3]))    # list red numbers
            #green.append('%s'%(split_tabs[4]))  # list green numbers
            #blue.append('%s'%(split_tabs[5]))   # list blue numbers
            f.write("%s %s %s\n"%(x,y,z))

            #Y_max
            if y > y_max:
                y_max = y
                highestPoint = ("%s\t%s\t%s"%(x,y_max,z))
 
            #Y_min
            if y < y_min:
                y_min = y
                lowestPoint = ("%s\t%s\t%s"%(x,y_min,z))
                
            #x_min
            if x < x_min:
                x_min = x
                most_leftPoint = ("%s\t%s\t%s"%(x_min,y,z))
                
            #x_max
            if x > x_max:
                x_max = x
                most_rightPoint = ("%s\t%s\t%s"%(x_max,y,z))
                
            #z_max
            if z > z_max:
                z_max = z
                z_maxPoint = ("%s\t%s\t%s"%(x,y,z_max))

            #z_min
            if z < z_min:
                z_min = z
                z_minPoint = ("%s\t%s\t%s"%(x,y,z_min))
        '''
        if number_columns == 4:
            a = (split_tabs[0])
            b = (split_tabs[1])
            c = (split_tabs[2])
            d = (split_tabs[3])
            f.write("%s %s %s %s\n"%(a,b,c,d))'''
                    
    #f.write("%s\n%s\n%s\n%s"%(lowestPoint,highestPoint,most_leftPoint,most_rightPoint))
    
    #print 'lowestPoint',lowestPoint
    #print 'highestPoint',highestPoint
    #print 'most_leftPoint',most_leftPoint
    #print 'most_rightPoint',most_rightPoint
    #print 'min_zPoint',z_minPoint
    #print 'max_zPoint', z_maxPoint
    #print x_co
    #print y_co
    #print z_co
    #print red
    #print green
    #print blue
    f.close()
    var4 = 'x'
    width(x_co,y_co,z_co,var4)
    var4 = 'z'
    width(z_co,y_co,x_co,var4)

    landmarkco(lowestPoint,highestPoint,most_leftPoint,most_rightPoint,z_minPoint,z_maxPoint)

#function for calculating the widest with
def width(var1,var2,var3,var4):

    #sorting of the lists on y (var2)
    var1_sort_var2, var2_sort_var2,var3_sort_var2 = zip(*sorted(zip(var1,var2,var3), key = operator.itemgetter(1),reverse = True)) # sort on y
    new_temp = []
    width = {} #dictionary for storing the y value with the width of either x or z

    for i in range(0, (len(var1))):
        
        if i == len(var1):      # for the last row
            try:
                width_var1 = (new_temp[0] - new_temp[-1])       #calculating the width
                width.update({var2_sort_var2[i-1]:width_var1})  # adding to dictionary
                new_temp = []                                   #clean new_temp variable
            except:
                break

        #calculating the width for y values    
        try:
            #if the previous number is the same as the following number, the var1 value is stored in the new_temp list
            if var2_sort_var2[i] == var2_sort_var2[i-1]:
                new_temp.append(float(var1_sort_var2[i-1]))
                new_temp.append(float(var1_sort_var2[i]))
                new_temp = sorted(new_temp, reverse = True) # the new_temp list is sorted                 
            else:
                width_var1 = (new_temp[0] - new_temp[-1]) # the max width is calculated by the highest number and the lowest number.
                width.update({var2_sort_var2[i-1]:width_var1}) # add to the dictionary with the y value of the max width
                new_temp = [] #clear new_temp list
        except:
            continue
        
    a = max(width.iteritems(), key=operator.itemgetter(1))[0]
    b = max(width.iteritems(), key=operator.itemgetter(1))[1]
    print 'The max width of %s is on y value: %s width: %s'%(var4,a,b)

#write landmarks coordinates to file
def landmarkco(lowestPoint,highestPoint,most_leftPoint,most_rightPoint,z_minPoint,z_maxPoint):
    
    lowestPoint = lowestPoint #min y
    highestPoint = highestPoint # max y
    most_leftPoint = most_leftPoint # min x
    most_rightPoint = most_rightPoint # max x
    z_minPoint = z_minPoint # min z
    z_maxPoint = z_maxPoint # max z

    #outputfile landmark coordinates
    outputLandmark = open('outputLandmarkM.txt', 'w')

    #headers of file
    number_of_individuals = 1 #this will be variable
    number_of_landmarks = 6 #this will be variable
    number_of_dimensions = 3 
    names = 'test1' # this will be variable

    #output write to file
    outputLandmark.write('[individuals]\n%s\n\n[landmarks]\n%s\n\n[dimensions]\n%s\n\n[names]\n%s\n'%(number_of_individuals,number_of_landmarks,number_of_dimensions,names))
    outputLandmark.write("\n[rawpoints]\n\n'%s\n\n"%(names))
    #coordinates
    outputLandmark.write("%s\n%s\n%s\n%s\n%s\n%s\n"%(lowestPoint,highestPoint,most_leftPoint,most_rightPoint,z_minPoint,z_maxPoint))
    #wireframe for morphologika
    outputLandmark.write("\n[wireframe]\n1 4\n4 2\n2 3\n3 1\n1 5\n5 2\n2 6\n6 1")
    #closing outputfile
    outputLandmark.close()

    
input_user()
#read_ply_file()
