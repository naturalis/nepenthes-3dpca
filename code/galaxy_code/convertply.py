#Converter for ply to ply in Galaxy.
#MB
#last update: 9-5-2014

#This programm extracts the enters of the header,
#caused by importing it to Galaxy.

import sys

# removing all the empty lines in the ply file

# Function main
def main():
    name_file_ply = sys.argv[1] # name of the ply file
    name_output = sys.argv[2] # name of the output file

    # open the input and output file
    file_ply = open(name_file_ply)
    output = open(str(name_output), 'w')

    lines = file_ply.readlines()
    file_ply.close()

    file_ply = open(name_file_ply) # re-open the file
    remove_empty_lines(lines, name_file_ply, output)

# Function remove empty line
def remove_empty_lines(lines,name_file_ply, output):
    file_ply = open(name_file_ply)
    for x in range(0,len(lines)):
        line = file_ply.readline().strip()
        line2 = line.strip().split()

        #writing all the correct lines to the ouputfile
        if len(line2) != 0:
            output.write('%s\n'%(line)) 

    output.close()

main()
