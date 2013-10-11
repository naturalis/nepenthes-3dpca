#Converter of dta to csv
#Mirna Baak
#baak.mirna@gmail.com
#9-10-2013
#last update: 9-10-2013

import sys
file_name = raw_input('Name file: ')
file_outputname = raw_input('Outputname: ')
#input_file_name = sys.argv[1]

def convert_dta(file_name,file_outputname):
    
    read_file = open(file_name, 'r') #open file
    a = len(read_file.readlines())
    read_file2 = open(file_name, 'r') # open file second time
    output = open(file_outputname,'w') #output file

    numberlandmarks = 0
    header = "" 

    #for loop, coordinates, number of landmarks and name of sample will be stored in csv format
    for x in range(0,a):
        b = read_file2.readline().strip()
        split_tabs = b.split('  ')
        number_columns = len(split_tabs)
        if x == 0:
            header += b       #name of sample     
        if number_columns == 3: #coordinates
            output.write("%s,%s,%s\n"%(float(split_tabs[0]),float(split_tabs[1]),float(split_tabs[2])))
            numberlandmarks += 1 # number of landmarks

    header += ", %s"%(str(numberlandmarks))
    output.write("%s"%(header)) # writing header to output file

    output.close()
    #outputname.close()
convert_dta(file_name,file_outputname)
            

