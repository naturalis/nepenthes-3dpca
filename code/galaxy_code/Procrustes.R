#Procrustes tool for performing procrustes analysis on landmark data
#MB

#commandline arguments
args <- commandArgs(TRUE)
#input 
input <- args[1]
nb_landmarks <- args[2]
nb_dimension <- 3
output <- args[3]
outputcentroid <- args[4]

#package geomorph
suppressMessages(library("geomorph"))

#reading input file (landmark coordinates)
read <- read.csv(file <- input,header = FALSE)

#creating good array with arrayspecs
new_array <- arrayspecs(read,as.integer(nb_landmarks),as.integer(nb_dimension))

#perform procrustes with gpagen
output_procrustes <- gpagen(A=new_array, ShowPlot= FALSE)
#turn array for PCA
output_procrustes_coo <- t(two.d.array(output_procrustes$coords))
#output procrustes coordinates
write.csv(output_procrustes_coo,output, row.names = FALSE)
#output procrustes centroid size
write.csv(output_procrustes$Csize,outputcentroid, row.names = FALSE)
