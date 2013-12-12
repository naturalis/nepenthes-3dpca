#Converter multiple .dta files to .csv file

from optparse import OptionParser
from os.path import basename


def main():
    parser = OptionParser()
    parser.add_option("--output")
    parser.add_option("--output2")
    parser.add_option("--input_file", action="append", default=[])
    parser.add_option("--input_name", action="append", default=[])


    (options, _) = parser.parse_args()

    header = ""
    header_temp = "" 
    # loop for running through the files, extract coordinates and header 
    with(open(options.output, "w")) as f:
	with(open(options.output2, "w")) as g:
            for i, (input_file, input_name) in enumerate(zip(options.input_file, options.input_name)):
            	for j, line in enumerate(open(input_file, "r").readlines()): # readlines
                    line = line.strip()
		    split_tabs = line.split('  ') # split on tabs
		    number_columns = len(split_tabs)
    		    if j == 0: #header
                    	header_temp = "%s" %(line.replace(' ', '_'))
			header += "%s\n"%(header_temp[1:-4]) #sample name
		      	
		    if number_columns == 3: #coordinates
                    	f.write("%f,%f,%f\n"%(float(split_tabs[0]),float(split_tabs[1]),float(split_tabs[2])))
	    g.write("%s\n"%(header)) # writing header to output file     #name of sample

if __name__ == "__main__":
    main()
