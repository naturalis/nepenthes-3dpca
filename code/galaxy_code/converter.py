# python 2.7
# MB
# Convertion multiple .dta files to one .csv file with coordinates
# and one .csv file with sample names.

from optparse import OptionParser
from os.path import basename

# Function for merging all files in .csv format 
# and extracting the headers of the files.
def main():
    # extracting the users input
    parser = OptionParser()
    parser.add_option("--output")
    parser.add_option("--output2")
    parser.add_option("--input_file", action="append", default=[]) # multiple inputfiles
    parser.add_option("--input_name", action="append", default=[]) # names of multiple inputfiles
    (options, _) = parser.parse_args()

    
    header = ""
    header_temp = "" 
    # open every file and concatenate the files
    with(open(options.output, "w")) as output:
	with(open(options.output2, "w")) as output2:
            for i, (input_file, input_name) in enumerate(zip(options.input_file, options.input_name)):
		# open a input file
            	for j, line in enumerate(open(input_file, "r").readlines()): 
                    line = line.strip()  
		    split_tabs = line.split('  ')
		    number_columns = len(split_tabs)
		    # extract name of sample
    		    if j == 0:
                    	header_temp = "%s" %(line.replace(' ', '_'))
			header += "%s\n"%(header_temp[1:-4])
		    # extract the coordinates  	
		    if number_columns == 3: 
                    	output.write("%f,%f,%f\n"%(float(split_tabs[0]),float(split_tabs[1]),float(split_tabs[2])))
	    output2.write("%s\n"%(header)) # writing header to output file     #name of sample

main()
