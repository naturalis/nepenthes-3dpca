args <- commandArgs(TRUE)
input <- args[1]
nb_landmarks <- args[2]
nb_species <- args[3]
output <- args[4]
#wil je er een plot bij?
suppressMessages(library("geomorph"))
read <- read.csv(file <- input,header = FALSE)
#
new_array <- arrayspecs(read,as.integer(nb_landmarks),as.integer(nb_species))
output_procrustes <- gpagen(A=new_array, ShowPlot= FALSE)
#png(output)
#write.table(pca1,output)
#suppressMessages(plot(pca1,pca2, pch=20,cex=1))

#dev.copy(png, output_coo)
#graphics.off()
#klopt dit nou?
output_procrustes_coo <- t(two.d.array(output_procrustes$coords))

write.csv(output_procrustes_coo,output, row.names = FALSE)
