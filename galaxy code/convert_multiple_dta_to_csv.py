#Converter of multiple dta files to one csv
#Mirna Baak
#baak.mirna@gmail.com
#13-11-2013
#last update: 13-11-2013

import sys
import os


file_outputname = sys.argv[1]
file_outputname2 = sys.argv[2]
file_name = sys.argv[3:]

def convert_dta(file_name,file_outputname,file_outputname2):
    output = open(file_outputname,'w') #output file
    output2 = open(file_outputname2, 'w')
    
    for x in range(0,len(file_name)):
        read_file = open(file_name[x], 'r') #open file
    	a = len(read_file.readlines())
    	read_file2 = open(file_name[x], 'r') # open file second time
    

    	numberlandmarks = 0
    	header = "" 

        #for loop, coordinates, number of landmarks and name of sample will be stored in csv format
        for x in range(0,a):
            b = read_file2.readline().strip()
            split_tabs = b.split('  ')
            number_columns = len(split_tabs)
            if x == 0:
                header += b.replace(' ', '_')     #name of sample     
            if number_columns == 3: #coordinates
                output.write("%f,%f,%f\n"%(float(split_tabs[0]),float(split_tabs[1]),float(split_tabs[2])))
                numberlandmarks += 1 # number of landmarks

        output2.write("%s\n"%(header[1:-4])) # writing header to output file

    output.close()

convert_dta(file_name,file_outputname,file_outputname2)
            

            

