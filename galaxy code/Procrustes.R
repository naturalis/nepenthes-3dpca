args <- commandArgs(TRUE)
input <- args[1]
nb_landmarks <- args[2]
nb_dimension <- args[3]
output <- args[4]
outputcentroid <- args[5]
#wil je er een plot bij?
suppressMessages(library("geomorph"))
read <- read.csv(file <- input,header = FALSE)

new_array <- arrayspecs(read,as.integer(nb_landmarks),as.integer(nb_dimension))
output_procrustes <- gpagen(A=new_array, ShowPlot= FALSE)

output_procrustes_coo <- t(two.d.array(output_procrustes$coords))

write.csv(output_procrustes_coo,output, row.names = FALSE)

write.csv(output_procrustes$Csize,outputcentroid, row.names = FALSE)
