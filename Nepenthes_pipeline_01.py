#Mirna Baak
#Nepenthes pitchers project Naturalis Internship
#19-9-2013
#version 01

# Read file .ply 
def read_ply_file():
    name_file = raw_input("file: ")                 # input name of file
    open_file = open(name_file, 'r')                # open file
    length_total_file = len(open_file.readlines())  # total number of lines
    open_file.close() # close file
    open_file2 = open(name_file, 'r')               # open file second time

    # seperate header
    header = ""
    for line in range(0,length_total_file):         # number of lines header
        data_line = open_file2.readline().strip()

        if data_line == 'end_header':               # the end of the header
            header = header + data_line + "\n"
            break

        else:
            header = header + data_line + "\n"      # lines header
    print header


    x_co = []   #x coordinates list
    y_co = []   #y coordinates list
    z_co = []   #z coordinates list
    red = []    # red value list
    green = []  # green value list
    blue = []   # blue value list

    #x, y and z coordinates in seperate lists

    for line_2 in range(0, length_total_file):

        coordinates = open_file2.readline().strip() # readline input file
        split_tabs = coordinates.split(' ')         # split into seperate fragments for each line
        number_columns = len(split_tabs)            # number of columns on a line

        if number_columns == 6: 
            x_co.append('%s'%(split_tabs[0]))   # list x coordinates
            y_co.append('%s'%(split_tabs[1]))   # list y coordinates
            z_co.append('%s'%(split_tabs[2]))   # list z coordinates
            red.append('%s'%(split_tabs[3]))    # list red numbers
            green.append('%s'%(split_tabs[4]))  # list green numbers
            blue.append('%s'%(split_tabs[5]))   # list blue numbers

        else:
            break

    print x_co
    print y_co
    print x_co
    print red
    print green
    print blue
        
read_ply_file()
